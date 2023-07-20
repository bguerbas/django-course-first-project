from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe, Category, User


# resolve -> qual função está sendo usada para renderizar a página
class RecipeViewsTest(TestCase):
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
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='user',
            last_name='user',
            username='user',
            password='23456',
            email='user@email.com')
        recipe = Recipe.objects.create(
            title='Title',
            description='Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
            category=category,
            author=author)
        response = self.client.get(reverse('recipes-home'))
        response_recipe = response.context['recipes'].first()
        self.assertEqual(response_recipe.title, recipe.title)

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
