from django.urls import path
from core.user.views import *

urlpatterns = [

    #Users
    path('list/',UserListView.as_view(),name='user_list'),
    path('create/',UserCreateView.as_view(),name='create_user'),
    path('update/<int:pk>/',UserUpdateView.as_view(),name='update_user'),
    path('delete/<int:pk>/',UserDeleteView.as_view(),name='delete_user'),
    path('change/group/<int:pk>',UserChangeGroup.as_view(),name='change_group'),
    path('profile/',UserProfileView.as_view(),name='profile_user'),
    path('change/password/',UserChangePasswordView.as_view(),name='change_password_user'),
]