from core.erp.mixins import isSuperUserMixin,ValidatePermissionRequiredMixin
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from core.erp.models import Category
from core.erp.forms import CategoryForm
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy


#Vista basade en Clase ListView
class CategoryListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):

    #Variables que controlan los permisos que se requieren para poder interactuar con la vista.
    permission_required = 'view_category'
    url_redirect = reverse_lazy('dashboard')

    #Se Define Modelo.
    model = Category

    #Se Define nombre del Template que contiene la lista.
    template_name = 'category/list.html'

    #Excepcion del token csrfmiddleware
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    #Metodo dispatch que se ejecuta cuando se llama a una vista y es el que se encarga de redireccionar ya sea para el metodo post o get dependiendo la peticion que se haga
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #Modificación metodo Post. Funcion que interactua con el formulario del template. Mediante la variable "request" se puede acceder a la informacion enviada en el formulario.
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
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)
    #Modificación de la funcion get_context_data. Se genera variable "context". Se asignan variables al diccionario context que pueden ser usadas en el template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of Categories'
        context['create_url'] = reverse_lazy('create_category')
        context['list_url'] = reverse_lazy('category_list')
        context['entity'] = 'Categories'
        context['dt_function'] = 'getCategoryData()'
        return context

class CategoryCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):

    #Variables que controlan los permisos que se requieren para poder interactuar con la vista.
    permission_required = 'add_category'
    url_redirect = reverse_lazy('category_list')

    #Se Define Modelo.
    model = Category
    #Se define la clase Form que se utilizara en el formulario.
    form_class = CategoryForm

    template_name = 'category/create.html'
    success_url = reverse_lazy('category_list')

    #Decorador que indica que se requiere estar logeado para poder interactuar con la vista.
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
        context['entity'] = 'Categories' 
        context['list_url'] = reverse_lazy('category_list')
        context['action'] = 'add'
        context['url_create'] = '/erp/category/create/'
        return context

class CategoryUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/edit.html'
    success_url = reverse_lazy('category_list')
    permission_required = 'change_category'
    url_redirect = reverse_lazy('category_list')

    @method_decorator(login_required)
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
        context['entity'] = 'Categories'
        context['action'] = 'edit'
        context['url_edit'] = '/erp/category/update/'
        return context

class CategoryDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Category
    template_name = 'category/delete.html'
    success_url = reverse_lazy('category_list')
    permission_required = 'delete_category'
    url_redirect = reverse_lazy('category_list')

    @method_decorator(login_required)
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
        context['entity'] = 'Categories'
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
        context['entity'] = 'Categories'
        context['list_url'] = reverse_lazy('category_list')
        context['action'] = 'add'
        return context
