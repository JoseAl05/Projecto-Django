from core.erp.views.test.views import TestView
from django.urls import path
from core.erp.views.category.views import *
from core.erp.views.product.views import *
from core.erp.views.dashboard.views import DashboardView

urlpatterns = [

    #Categories
    path('category/list/',CategoryListView.as_view(),name='category_list'),
    path('category/create/',CategoryCreateView.as_view(),name='create_category'),
    path('category/update/<int:pk>/',CategoryUpdateView.as_view(),name='update_category'),
    path('category/delete/<int:pk>/',CategoryDeleteView.as_view(),name='delete_category'),
    path('category/form/',CategoryFormView.as_view(),name='form_category'),

    #Products
    path('product/list/',ProductListView.as_view(),name='product_list'),
    path('product/create/',ProductCreateView.as_view(),name='create_product'),
    path('product/update/<int:pk>/',ProductUpdateView.as_view(),name='update_product'),
    path('product/delete/<int:pk>/',ProductDeleteView.as_view(),name='delete_product'),
    path('product/form/',ProductFormView.as_view(),name='form_product'),

    #Dashboard
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path('test/',TestView.as_view(),name='test'),
]
