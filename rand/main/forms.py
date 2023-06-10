from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'USERNAME'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'PASSWORD'
            }
        )
    )


class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_check'
        ]

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'USERNAME'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'PASSWORD'
            }
        )
    )
    password_check = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'REPEAT PASSWORD'
            }
        )
    )

    def clean_password_check(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_check']:
            raise forms.ValidationError('Passwords don\'t match!')
        return cd['password_check']