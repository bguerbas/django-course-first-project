from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


# resolve -> qual função está sendo usada para renderizar a página
class RecipeCategoryViewTest(RecipeTestBase):

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        url = reverse(
            'recipes:category',
            kwargs={'category_id': recipe.category.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        # Need a recipe for this test
        needed_title = 'This is a category test'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse(
            'recipes:category',
            kwargs={'category_id': 1})
        )
        content = response.content.decode('utf-8')

        # Check if one recipe is loaded
        self.assertIn(needed_title, content)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        url = reverse('recipes:category', kwargs={'category_id': 1000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
