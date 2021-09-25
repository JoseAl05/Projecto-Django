from django.urls import path
from core.erp.views.category.views import *
from core.erp.views.dashboard.views import DashboardView

urlpatterns = [

    #Categories
    path('category/list/',CategoryListView.as_view(),name='category_list'),
    path('category/create/',CategoryCreateView.as_view(),name='create_category'),
    path('category/update/<int:pk>/',CategoryUpdateView.as_view(),name='update_category'),
    path('category/delete/<int:pk>/',CategoryDeleteView.as_view(),name='delete_category'),
    path('category/form/',CategoryFormView.as_view(),name='form_category'),

    #Dashboard
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
]
