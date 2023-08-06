from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


# resolve -> qual função está sendo usada para renderizar a página
class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        # mesma coisa -> resolve('/'), porém se a url mudar,
        # o teste continua funcionando.
        view = resolve(reverse('recipes:home'))
        self.assertEqual(view.func, views.home)

    # Testando o template usado e status da response
    def test_recipe_home_view_returns_status_code_200(self):
        url = reverse('recipes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_uses_correct_template(self):
        url = reverse('recipes:home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_shows_no_recipes_found_if_no_recipes(self):
        url = reverse('recipes:home')
        response = self.client.get(url)
        self.assertIn(
            '<h1>No recipes found here.</h1>',
            response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe(category_data={'name': 'Breakfast'})
        response = self.client.get(reverse('recipes:home'))
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
        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            '<h1>No recipes found here.</h1>',
            response.content.decode('utf-8'))
