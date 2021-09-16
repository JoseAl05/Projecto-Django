from django.shortcuts import render
from core.erp.models import Category

def category_list(request):
    data= {
        'title': 'Listado de Categorías',
        'categories': Category.objects.all()
    }
    return render(request,'category/list.html',data)

def myFirstView(request):
    data = {
        'name':'Jose'
    }
    return render(request,'home.html',data)

def mySecondView(request):
    return render(request,'index.html')