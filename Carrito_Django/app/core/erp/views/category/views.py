from django.shortcuts import render
from core.erp.models import Category
from django.views.generic import ListView

def category_list(request):
    data= {
        'title': 'Listado de Categorías',
        'categories': Category.objects.all()
    }
    return render(request,'category/list.html',data)

class CategoryListView(ListView):
    model = Category
    template_name = 'category/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of Categories' 
        return context
    



# def myFirstView(request):
#     data = {
#         'name':'Jose'
#     }
#     return render(request,'home.html',data)

# def mySecondView(request):
#     return render(request,'index.html')