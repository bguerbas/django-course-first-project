from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views


# resolve -> qual função está sendo usada para renderizar a página
class RecipeViewsTest(TestCase):
    def test_recipe_home_views_function_is_correct(self):
        # mesma coisa -> resolve('/'), porém se a url mudar,
        # o teste continua funcionando.
        view = resolve(reverse('recipes-home'))
        self.assertEqual(view.func, views.home)

    def test_recipe_category_views_function_is_correct(self):
        view = resolve(reverse('recipes-category', kwargs={'category_id': 1}))
        self.assertEqual(view.func, views.category)

    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(reverse('recipes-recipe', kwargs={'id': 1}))
        self.assertEqual(view.func, views.recipe)

    # Testando o template usado e status da response
    def _recipe_home_view_returns_status_code_200(self):
        url = reverse('recipes-home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def _recipe_home_view_uses_correct_template(self):
        url = reverse('recipes-home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
