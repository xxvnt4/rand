from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import LoginForm, SignupForm

from .models import Topics


def index(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html')
    else:
        return redirect('user_login')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(
                    username=cd['username'],
                    password=cd['password']
                )
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    form = LoginForm()
                    return render(
                        request,
                        'main/user_login.html',
                        {
                            'form': form,
                            'disabled': 1
                        }
                    )
            else:
                form = LoginForm()
                return render(
                    request,
                    'main/user_login.html',
                    {
                        'form': form,
                        'disabled': 2
                    }
                )
        else:
            form = LoginForm()
        return render(
            request,
            'main/user_login.html',
            {
                'form': form,
                'disabled': ''
            }
        )

def user_signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.set_password(form.cleaned_data['password'])
                new_user.save()

                cd = form.cleaned_data
                user = authenticate(
                    username=cd['username'],
                    password=cd['password']
                )
                login(request, user)
                return redirect('index')
        else:
            form = SignupForm()

        return render(
            request,
            'main/user_signup.html',
            {
                'form': form
            }
        )


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('user_login')


def user_list(request):
    if request.user.is_authenticated:
        items = Topics.objects.filter(author=request.user)

        return render(
            request,
            'main/user_list.html',
            {
                'items': items
            }
        )
    else:
        return redirect('user_list')