from datetime import datetime
from random import choice

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from .forms import LoginForm, SignupForm, TopicsForm, UserForm
from .models import Topics

class TopicsList(ListView):
    model = Topics
    template_name = 'main/user_list.html'
    context_object_name = 'topics'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

def index(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html')

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
        topics = Topics.objects.filter(author=request.user).order_by('-date_created')

        if len(topics) == 0:
            return redirect('add_topic')

        pagination = Paginator(topics, 5)
        pages_amount = pagination.num_pages
        pages_num = request.GET.get('page', 1)
        range_page = pagination.page_range

        try:
            page = pagination.page(pages_num)
        except EmptyPage:
            page = pagination.page(1)

        return render(
            request,
            'main/user_list.html',
            {
                'topics': page,
                'pages_amount': pages_amount,
                'range_page': range_page
            }
        )

    return redirect('user_login')


@csrf_exempt
def add_topic(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            form = TopicsForm(request.POST)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()
                return redirect('user_list')
            else:
                error = 'Error!'

        form = TopicsForm()

        return render(
            request,
            'main/add_topic.html',
            {
                'form': form
            }
        )

    return redirect('user_login')


def random(request):
    if request.user.is_authenticated:
        topics = Topics.objects.filter(author=request.user)

        if len(topics) <= 1:
            return redirect('add_topic')

        available_ids = list(Topics.objects.filter(is_watched=False).values_list('id', flat=True))

        if len(available_ids) == 0:
            return redirect('confirm_reset_random')

        random_id = choice(available_ids)

        random_topic = Topics.objects.get(id=random_id)
        random_topic.date_watched = datetime.now()
        random_topic.is_watched = True
        random_topic.save()

        return redirect(reverse('topic_info', args=[random_id]))

    return redirect('user_login')


def topic_info(request, id):
    if request.user.is_authenticated:
        topic = Topics.objects.filter(id=id)[0]
        return render(
            request,
            'main/topic_info.html',
            {
                'topic': topic
            }
        )

    return redirect('user_login')


@csrf_exempt
def edit_topic(request, id):
    if request.user.is_authenticated:
        topic = Topics.objects.get(id=id)

        if request.method == 'POST':
            form = TopicsForm(request.POST, instance=topic)
            if form.is_valid():
                form.save()
                topic.date_updated = datetime.now()
                topic.save()

                return redirect(reverse('topic_info', args=[id]))

        form = TopicsForm(instance=topic)

        return render(
            request,
            'main/edit_topic.html',
            {
                'id': id,
                'form': form
            }
        )

    return redirect('user_login')


def confirm_delete_topic(request, id):
    if request.user.is_authenticated:
        topic = Topics.objects.get(id=id)

        return render(
            request,
            'main/confirm_delete.html',
            {'topic': topic}
        )

    return redirect('user_login')


def delete_topic(request, id):
    if request.user.is_authenticated:
        topic = Topics.objects.get(id=id)
        topic.delete()

        return redirect('user_list')

    return redirect('user_login')


def settings(request):
    if request.user.is_authenticated:
        return render(request, 'main/settings.html')

    return redirect('user_login')


def change_username(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)

        if request.method == 'POST':
            form = UserForm(request.POST, instance=user)

            if form.is_valid():
                form.save()
                user.save()

                return redirect('settings')

        form = UserForm(instance=user)

        return render(
            request,
            'main/change_username.html',
            {
                'form': form
            }
        )
    return redirect('user_login')


def confirm_delete_profile(request):
    if request.user.is_authenticated:
        return render(request, 'main/confirm_delete_profile.html')

    return redirect('user_login')


def delete_profile(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        user.delete()

    return redirect('user_login')


def confirm_reset_random(request):
    return render(
        request,
        'main/confirm_reset_random.html'
    )


def reset_random(request):
    topics = Topics.objects.all()

    for topic in topics:
        topic.is_watched = False
        topic.save()

    return redirect('random')
