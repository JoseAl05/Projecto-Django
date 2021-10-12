from django.http.response import HttpResponseRedirect, JsonResponse
from django.http import HttpResponse
from django.shortcuts import render,redirect
from core.erp.models import DetSale
from core.erp.models import Product
from core.erp.models import Sale
from core.erp.forms import SaleForm
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt 
from django.urls import reverse_lazy
from django.db import transaction
import json
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


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
                    #item['value'] = i.name
                    item['text'] = i.name
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
        context['detail'] = []
        return context

class SaleUpdateView(UpdateView):
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
                    print(data)

            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])

                    sale = Sale.objects.get(pk=self.get_object().id)
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    sale.detsale_set.all().delete()
                    
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
            else:
                data['error'] = 'You have not entered any option'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)   

    def get_details_product(self):
        data = []
        try:
            for i in DetSale.objects.filter(sale_id = self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)
                print(item)
        except:
            pass
        return data
            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['title'] = 'Update Sale'
        context['entity'] = 'Sales' 
        context['list_url'] = reverse_lazy('sale_list')
        context['action'] = 'edit'
        context['url_create'] = '/erp/sale/create/'
        context['detail'] = json.dumps(self.get_details_product())
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

class SaleInvoicePDFView(View):
    def get(self,request,*args,**kwargs):
        try:
            template = get_template('sale/invoice_pdf.html')
            context = {'title':'PDF'}
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response)
            return response;
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('sale_list'))