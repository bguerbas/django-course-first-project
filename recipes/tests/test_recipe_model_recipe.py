from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Category name'),
            author=self.make_author(username='newuser'),
            title='Recipe title',
            description='Recipe description',
            slug='recipe-slug-for-no-defaults',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=2,
            servings_unit='Porções',
            preparation_steps='Recipe preparation steps'
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65)
    ])
    def test_recipe_fields_max_length(self, field, max_lentgh):
        # funciona de forma dinamica, do que recipe.field = 'a' * 66 (field não mudará)  # noqa: E501
        setattr(self.recipe, field, 'a' * (max_lentgh + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='preparation_steps_is_html should be False by default'
            )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.is_published,
            msg='is_published should be False by default'
            )

    def test_recipe_string_representation(self):
        needed = 'Test Representation'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), needed,
            msg=f'Recipe string representation should be the "{needed}"'
            )
