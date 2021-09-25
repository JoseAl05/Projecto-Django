from django.contrib.auth.views import LogoutView
from django.urls import path
from core.login.views import LoginFormView,LoginFormView2,LogoutRedirectView

urlpatterns = [
    path('',LoginFormView.as_view(),name='login'),
    #path('logout/',LogoutView.as_view(),name='logout'),
    path('logout/',LogoutRedirectView.as_view(),name='logout'),
]
