from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from core.erp.models import DetSale
from core.erp.models import Product
from core.erp.models import Sale
from core.erp.forms import SaleForm
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,FormView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt 
from django.urls import reverse_lazy
from django.db import transaction
import json


class SaleListView(ListView):

    #Se Define Modelo.
    model = Sale

    #Se Define nombre del Template que contiene la lista.
    template_name = 'sale/list.html'

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
                for i in Sale.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_product':
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)
    
    #Modificación de la funcion get_context_data. Se genera variable "context". Se asignan nombres la lista para poder ser ocupadas en el template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of Sales' 
        context['create_url'] = reverse_lazy('create_sale')
        context['list_url'] = reverse_lazy('sale_list')
        context['entity'] = 'Sales'
        context['dt_function'] = 'getSaleData()'
        print(context)
        return context

class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('sale_list')


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_product':
                data = []
                products = Product.objects.filter(name__icontains = request.POST['term'])[0:10]
                for i in products:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])

                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()

                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['title'] = 'Create Sale'
        context['entity'] = 'Sales' 
        context['list_url'] = reverse_lazy('sale_list')
        context['action'] = 'add'
        context['url_create'] = '/erp/sale/create/'
        return context

class SaleDeleteView(DeleteView):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('sale_list')

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
        context['title'] = 'Delete Sale' 
        context['create_url'] = reverse_lazy('create_sale')
        context['list_url'] = reverse_lazy('sale_list')
        context['entity'] = 'Sales'
        context['action'] = 'delete'
        return context