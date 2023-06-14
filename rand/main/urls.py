from django.contrib.auth.views import LogoutView
from django.template.backends import django
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views
from .views import TopicsList, TopicInfoView, MyLogoutView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]

urlpatterns += [
    path('', views.index, name='index'),
    path('user_list/', TopicsList.as_view(), name='user_list'),
    path('add_topic/', views.TopicsCreate.as_view(), name='add_topic'),
    path('random/', views.random, name='random'),
    path('settings/', views.settings, name='settings'),
    path('change_username/', views.change_username, name='change_username'),
    path('confirm_delete_profile/', views.confirm_delete_profile, name='confirm_delete_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('confirm_reset_random/', views.confirm_reset_random, name='confirm_reset_random'),
    path('reset_random/', views.reset_random, name='reset_random'),
]

urlpatterns += [
    re_path(r'^topic_info/(?P<pk>\d+)/$', views.TopicInfoView.as_view(), name='topic_info'),
    re_path(r'^edit_topic/(?P<pk>\d+)/$', views.TopicsUpdate.as_view(), name='edit_topic'),
    re_path(r'^confirm_delete_topic/(?P<id>\d+)/$', views.confirm_delete_topic, name='confirm_delete_topic'),
    re_path(r'^delete_topic/(?P<id>\d+)/$', views.TopicsDelete.as_view(), name='delete_topic'),
]

urlpatterns += [
    path('', include('django.contrib.auth.urls')),
    path('my_logout/', MyLogoutView.as_view(), name='logout'),
]
