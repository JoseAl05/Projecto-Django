from django.http.response import JsonResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from core.erp.models import Category
from core.erp.forms import CategoryForm
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from django.urls import reverse_lazy


#Vista basade en Clase ListView
class CategoryListView(ListView):
    #Se Define Modelo.
    model = Category

    #Se Define nombre del Template que contiene la lista.
    template_name = 'category/list.html'

    #Excepcion del token csrfmiddleware
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #Modificación metodo Post
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Category.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
            #data = Category.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)
    
    #Modificación de la funcion get_context_data. Se genera variable "context". Se asignan nombres la lista para poder ser ocupadas en el template.
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
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['title'] = 'Create Category'
        context['entity'] = 'Categorías' 
        context['list_url'] = reverse_lazy('category_list')
        context['action'] = 'add' 
        return context

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/edit.html'
    success_url = reverse_lazy('category_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Category' 
        context['create_url'] = reverse_lazy('create_category')
        context['list_url'] = reverse_lazy('category_list')
        context['entity'] = 'Categorías'
        context['action'] = 'edit'
        return context

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/delete.html'
    success_url = reverse_lazy('category_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Category' 
        context['create_url'] = reverse_lazy('create_category')
        context['list_url'] = reverse_lazy('category_list')
        context['entity'] = 'Categorías'
        context['action'] = 'delete'
        return context

class CategoryFormView(FormView):
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        print(form.errors)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['title'] = 'Form Category'
        context['entity'] = 'Categorías' 
        context['list_url'] = reverse_lazy('category_list')
        context['action'] = 'add' 
        return context
