from django.urls import path
from core.erp.views.category.views import category_list

urlpatterns = [
    path('category/list',category_list,name='category_list'),
]
