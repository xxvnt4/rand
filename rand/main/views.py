from datetime import datetime
from random import choice

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView

from .forms import TopicsForm, UserForm, SignUpForm
from .models import Topics


class LoginView(LoginRequiredMixin, FormView):
    success_url = reverse_lazy('index')


class MyLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return redirect('login')


class TopicsList(ListView):
    model = Topics
    template_name = 'main/user_list.html'
    context_object_name = 'topics'
    paginate_by = 10
    allow_empty = False

    def get_queryset(self):
        return Topics.objects.filter(author=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            return redirect('add_topic')


class TopicInfoView(generic.DetailView):
    model = Topics
    template_name = 'main/topic_info.html'
    context_object_name = 'topic'

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            return redirect('add_topic')


def index(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html')

    return redirect('login')


@login_required
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
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
        form = SignUpForm()

    return render(
        request,
        'registration/signup.html',
        {
            'form': form
        }
    )


@csrf_exempt
@login_required
def add_topic(request):
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


@login_required
def random(request):
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


@csrf_exempt
@login_required
def edit_topic(request, id):
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
            'form': form,
            'topic': topic
        }
    )


@login_required
def confirm_delete_topic(request, id):
    topic = Topics.objects.get(id=id)

    return render(
        request,
        'main/confirm_delete.html',
        {'topic': topic}
    )


@login_required
def delete_topic(request, id):
    topic = Topics.objects.get(id=id)
    topic.delete()

    return redirect('user_list')


@login_required
def settings(request):
    return render(request, 'main/settings.html')


@login_required
def change_username(request):
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


@login_required
def confirm_delete_profile(request):
    return render(request, 'main/confirm_delete_profile.html')


@login_required
def delete_profile(request):
    user = User.objects.get(username=request.user)
    user.delete()


@login_required
def confirm_reset_random(request):
    return render(
        request,
        'main/confirm_reset_random.html'
    )


@login_required
def reset_random(request):
    topics = Topics.objects.all()

    for topic in topics:
        topic.is_watched = False
        topic.save()

    return redirect('random')
