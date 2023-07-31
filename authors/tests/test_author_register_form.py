from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from parameterized import parameterized
from authors.forms import RegisterForm


class AuthorRegisterFormUnitTests(TestCase):

    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_help_test(self, field, needed):
        form = RegisterForm()
        current = form[field].field.widget.attrs['placeholder']

        self.assertEqual(current, needed)

    @parameterized.expand([
        ('username', 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'),  # noqa: E501
        ('email', 'The e-mail must be valid.'),
        ('password', (
            'Password must have at least:\n * one uppercase letter\n '
            '* one lowercase letter\n * one number\n * 8 characters'
        )),
    ])
    def test_first_name_placefolder(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text

        self.assertEqual(current, needed)

    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('password', 'Password'),
        ('password2', 'Password confirmation'),
    ])
    def test_fields_labels(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label

        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'User',
            'last_name': 'Test',
            'email': 'usertest@email.com',
            'password': '*STRONGpassword123',
            'password2': '*STRONGpassword123',
        }
        return super().setUp(*args, **kwargs)
    
    def test_field_cannot_be_empty(self):
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)