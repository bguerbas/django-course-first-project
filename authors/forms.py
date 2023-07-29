from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        # '__all__' traz todos os campos do model
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

