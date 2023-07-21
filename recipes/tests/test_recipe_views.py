from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


# resolve -> qual função está sendo usada para renderizar a página
class RecipeViewsTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        # mesma coisa -> resolve('/'), porém se a url mudar,
        # o teste continua funcionando.
        view = resolve(reverse('recipes-home'))
        self.assertEqual(view.func, views.home)

    # Testando o template usado e status da response
    def test_recipe_home_view_returns_status_code_200(self):
        url = reverse('recipes-home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_uses_correct_template(self):
        url = reverse('recipes-home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_shows_no_recipes_found_if_no_recipes(self):
        url = reverse('recipes-home')
        response = self.client.get(url)
        self.assertIn(
            '<h1>No recipes found here.</h1>',
            response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe(category_data={'name': 'Breakfast'})
        response = self.client.get(reverse('recipes-home'))
        response_context = response.context['recipes']
        content = response.content.decode('utf-8')

        # Check if one recipe is loaded
        self.assertIn('Recipe Title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)
        self.assertIn('Breakfast', content)
        self.assertEqual(len(response_context), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        # Need recipe for this test
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes-home'))

        self.assertIn(
            '<h1>No recipes found here.</h1>',
            response.content.decode('utf-8'))

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        url = reverse(
            'recipes-category',
            kwargs={'category_id': recipe.category.id}
            )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        # Need a recipe for this test
        needed_title = 'This is a category test'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse(
            'recipes-category',
            kwargs={'category_id': 1})
            )
        content = response.content.decode('utf-8')

        # Check if one recipe is loaded
        self.assertIn(needed_title, content)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes-category', kwargs={'category_id': 1}))
        self.assertEqual(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes-recipe', kwargs={'id': 1}))
        self.assertEqual(view.func, views.recipe)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        url = reverse('recipes-category', kwargs={'category_id': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_returns_404_if_no_recipe_found(self):
        url = reverse('recipes-recipe', kwargs={'id': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        # Need a recipe for this test
        needed_title = 'This is a detail page - It load one recipe'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes-recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        # Check if one recipe is loaded
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)
        url = reverse(
            'recipes-recipe',
            kwargs={'id': recipe.id}
            )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
