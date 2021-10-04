from core.erp.mixins import isSuperUserMixin
from django.http.response import JsonResponse,HttpResponseRedirect
from core.erp.models import Product
from core.erp.forms import ProductForm
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from django.urls import reverse_lazy



#Vista basade en Clase ListView
class ProductListView(isSuperUserMixin,ListView):
    #Se Define Modelo.
    model = Product

    #Se Define nombre del Template que contiene la lista.
    template_name = 'product/list.html'

    #Excepcion del token csrf middleware
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #Modificación metodo Post
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            print(request.POST)
            print(request.FILES)
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Product.objects.all():
                    print(i)
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)
    
    #Modificación de la funcion get_context_data. Se genera variable "context". Se asignan nombres la lista para poder ser ocupadas en el template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of Products' 
        context['create_url'] = reverse_lazy('create_product')
        context['list_url'] = reverse_lazy('product_list')
        context['entity'] = 'Products'
        context['dt_function'] = 'getProductData()'
        return context

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('product_list')

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
        context['title'] = 'Create Product'
        context['entity'] = 'Products' 
        context['list_url'] = reverse_lazy('product_list')
        context['action'] = 'add'
        context['url_create'] = '/erp/product/create/'
        return context

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/edit.html'
    success_url = reverse_lazy('product_list')

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
        context['title'] = 'Update Product' 
        context['create_url'] = reverse_lazy('create_product')
        context['list_url'] = reverse_lazy('product_list')
        context['entity'] = 'Products'
        context['action'] = 'edit'
        context['url_edit'] = '/erp/product/update/'
        return context

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('product_list')

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
        context['title'] = 'Delete Product' 
        context['create_url'] = reverse_lazy('create_product')
        context['list_url'] = reverse_lazy('product_list')
        context['entity'] = 'Products'
        context['action'] = 'delete'
        return context

class ProductFormView(FormView):
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        print(form.errors)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['title'] = 'Form Product'
        context['entity'] = 'Products' 
        context['list_url'] = reverse_lazy('product_list')
        context['action'] = 'add' 
        return context
