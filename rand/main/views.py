from datetime import datetime
from random import choice

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import Http404, QueryDict, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, FormView, CreateView, UpdateView, DeleteView

from .forms import TopicsForm, UserForm, SignUpForm
from .models import Topics


class LoginView(FormView):
    success_url = reverse_lazy('index')


class MyLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return redirect('login')


class TopicsList(LoginRequiredMixin, ListView):
    model = Topics
    template_name = 'main/user_list.html'
    context_object_name = 'topics'
    paginate_by = 10
    allow_empty = False

    empty_search = False
    search = None
    action = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sort_order = self.request.GET.get('sort', 'date_created')
        queryset = self.get_queryset()
        self.action = self.request.GET.get('action')

        if sort_order == 'title':
            queryset = queryset.order_by('title')

        if sort_order == '-title':
            queryset = queryset.order_by('-title')

        if sort_order == 'date_created':
            queryset = queryset.order_by('date_created')

        if sort_order == '-date_created':
            queryset = queryset.order_by('-date_created')

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        context['topics'] = queryset
        context['paginator'] = paginator
        context['sort_order'] = sort_order
        context['empty_search'] = self.empty_search
        context['search'] = self.search
        context['action'] = self.action
        context['query_string'] = self.request.META['QUERY_STRING']

        return context

    def get_queryset(self):
        search_text = self.request.GET.get('search')

        if search_text:
            self.search = search_text

        user_topics = self.model.objects.filter(author=self.request.user)

        if search_text:
            searched_topics = user_topics.filter(
                Q(title__icontains=search_text) |
                Q(subtitle__icontains=search_text) |
                Q(description__icontains=search_text)
            )
            if searched_topics:
                return searched_topics
            else:
                self.empty_search = True

        return user_topics

    def get(self, request, *args, **kwargs):
        query_params = QueryDict(mutable=True)
        for key in self.request.GET.keys():
            values = self.request.GET.getlist(key)
            if len(values) > 1:
                query_params.setlist(key, [values[-1]])
            else:
                query_params[key] = values[0]

        if query_params != self.request.GET:
            url = request.path + '?' + query_params.urlencode()
            return HttpResponseRedirect(url)

        return super().get(request, *args, **kwargs)


    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            return redirect('add_topic')

class TopicView(View):

    def get(self, request):
        objects = Topics.objects.all()

        return render()


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


class TopicsCreate(LoginRequiredMixin, CreateView):
    model = Topics
    form_class = TopicsForm
    template_name = 'main/add_topic.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = self.request.user
        object.save()

        return super().form_valid(form)


class TopicsUpdate(LoginRequiredMixin, UpdateView):
    model = Topics
    form_class = TopicsForm
    template_name = 'main/edit_topic.html'
    success_url = reverse_lazy('user_list')


class TopicsDelete(LoginRequiredMixin, DeleteView):
    model = Topics
    success_url = reverse_lazy('user_list')


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
def confirm_delete_topic(request, pk):
    topic = Topics.objects.get(id=pk)

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


@login_required
def do_with_selected(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        Topics.objects.filter(id__in=selected_items).delete()

        url = reverse('user_list') + '?action=edit'

        return redirect(url)
