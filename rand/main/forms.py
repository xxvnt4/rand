from django import forms
from django.contrib.auth.models import User

from .models import Topics


class SignUpForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_check',
            'email'
        ]

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'USERNAME'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'EMAIL'
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


class TopicsForm(forms.ModelForm):

    class Meta:
        model = Topics
        fields = [
            'title',
            'subtitle',
            'description',
            'link'
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'TITLE'
                }
            ),
            'subtitle': forms.TextInput(
                attrs={
                    'placeholder': 'SUBTITLE'
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'placeholder': 'DESCRIPTION'
                }
            ),
            'link': forms.URLInput(
                attrs={
                    'placeholder': 'SOURCE'
                }
            )
        }

    def clean_title(self):
        return self.cleaned_data['title'].upper()

    def clean_subtitle(self):
        return self.cleaned_data['subtitle'].upper()

    def clean_description(self):
        return self.cleaned_data['description']

    def clean_link(self):
        return self.cleaned_data['link']


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'NEW USERNAME'
                }
            )
        }

    def clean_username(self):
        return self.cleaned_data['username']