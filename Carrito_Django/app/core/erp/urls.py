from django.urls import path
from core.erp.views.category.views import *

urlpatterns = [
    path('category/list/',CategoryListView.as_view(),name='category_list'),
    path('category/list2/',category_list,name='category_list2'),
    path('category/create/',CategoryCreateView.as_view(),name='create_category'),
]
