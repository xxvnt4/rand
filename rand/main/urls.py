from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.user_signup, name='user_signup'),
    path('logout/', views.user_logout, name='user_logout'),
    path('user_list/', views.user_list, name='user_list'),
    path('add_topic/', views.add_topic, name='add_topic'),
    path('random/', views.random, name='random'),
    path('topic_info/<id>/', views.topic_info, name='topic_info'),
    path('edit_topic/<id>/', views.edit_topic, name='edit_topic'),
    path('confirm_delete_topic/<id>', views.confirm_delete_topic, name='confirm_delete_topic'),
    path('delete_topic/<id>', views.delete_topic, name='delete_topic'),
    path('settings/', views.settings, name='settings'),
    path('change_username/', views.change_username, name='change_username'),
    path('confirm_delete_profile/', views.confirm_delete_profile, name='confirm_delete_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
]