from django.urls import path, re_path

from . import views
from .views import TopicsList


urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.user_signup, name='user_signup'),
    path('logout/', views.user_logout, name='user_logout'),
]

urlpatterns += [
    path('', views.index, name='index'),
    path('user_list/', TopicsList.as_view(), name='user_list'),
    path('add_topic/', views.add_topic, name='add_topic'),
    path('random/', views.random, name='random'),
    path('settings/', views.settings, name='settings'),
    path('change_username/', views.change_username, name='change_username'),
    path('confirm_delete_profile/', views.confirm_delete_profile, name='confirm_delete_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('confirm_reset_random/', views.confirm_reset_random, name='confirm_reset_random'),
    path('reset_random/', views.reset_random, name='reset_random'),
]

urlpatterns += [
    re_path(r'^topic_info/(?P<id>\d+)/$', views.topic_info, name='topic_info'),
    re_path(r'^edit_topic/(?P<id>\d+)/$', views.edit_topic, name='edit_topic'),
    re_path(r'^confirm_delete_topic/(?P<id>\d+)/$', views.confirm_delete_topic, name='confirm_delete_topic'),
    re_path(r'^delete_topic/(?P<id>\d+)/$', views.delete_topic, name='delete_topic'),
]
