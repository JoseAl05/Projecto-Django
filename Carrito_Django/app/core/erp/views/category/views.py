from django.http.response import JsonResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from core.erp.models import Category
from core.erp.forms import CategoryForm
from django.views.generic import ListView,CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from django.urls import reverse_lazy

def category_list(request):
    data= {
        'title': 'Listado de Categorías',
        'categories': Category.objects.all()
    }
    return render(request,'category/list.html',data)

class CategoryListView(ListView):
    model = Category
    template_name = 'category/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = Category.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of Categories' 
        context['create_url'] = reverse_lazy('create_category')
        context['list_url'] = reverse_lazy('category_list')
        context['entity'] = 'Categorías'
        return context

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('category_list')

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return render(request,self.template_name,context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Category'
        context['entity'] = 'Categorías' 
        context['list_url'] = reverse_lazy('category_list')
        return context
    



# def myFirstView(request):
#     data = {
#         'name':'Jose'
#     }
#     return render(request,'home.html',data)

# def mySecondView(request):
#     return render(request,'index.html')