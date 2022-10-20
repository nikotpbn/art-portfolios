from django.contrib.auth.hashers import make_password
from django import forms
from .models import User


class LoginForm(forms.ModelForm):
    # Name field
    email = forms.EmailField(
        label='email',
        max_length=256,
        required=True,
        error_messages={
            'required': 'O email não pode ser vazio',
            'invalid': 'Email inválido'
        }
    )

    password = forms.CharField(
        label='Senha',
        min_length=3,
        max_length=32,
        widget=forms.PasswordInput(),
        required=True,
        error_messages={
            'required': 'A senha não foi preenchida',
            'min_length': 'Senha incorreta'
        }
    )

    # This class sets the fields that should be in the views.
    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]
