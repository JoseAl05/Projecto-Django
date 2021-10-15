from django.urls.base import reverse_lazy
from django.views.generic import TemplateView
from datetime import datetime
from core.erp.models import DetSale
from core.erp.models import Product
from core.erp.models import Sale
from django.db.models.functions import Coalesce
from django.db.models import Sum, Value as V
from django.db.models.fields import DecimalField
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt 
from random import randint


class DashboardView(TemplateView):
    template_name = 'dashboard.html'


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def get_graph_sales_monthly(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1,13):
                total = Sale.objects.filter(date_joined__year=year,date_joined__month=m).aggregate(sum_total=Coalesce(Sum('total'),V(0),output_field=DecimalField()))
                data.append(float(total['sum_total']))
        except:
            pass
        return data

    def get_graph_sales_products_year_month(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for i in Product.objects.all():
                total = DetSale.objects.filter(sale__date_joined__year=year,sale__date_joined__month=month,prod_id = i.id).aggregate(sum_subtotal=Coalesce(Sum('subtotal'),V(0),output_field=DecimalField()))
                if float(total['sum_subtotal']) > 0:
                    data.append({
                        'name':i.name,
                        'y':float(total['sum_subtotal'])
                    })
        except:   
            pass
        return data

    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_sales_monthly':
                data = {
                    'name':'Sale Percentage',
                    'showInLegend':False,
                    'colorByPoint':True,
                    'data': self.get_graph_sales_monthly()
                }
            elif action == 'get_graph_sales_products_year_month':
                data = {
                    'name':'Percentage',
                    'colorByPoint':True,
                    'data': self.get_graph_sales_products_year_month()
                }
            else:
                data['error'] = 'Error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Admin Panel'
        context['entity'] = 'Categories' 
        context['list_url'] = reverse_lazy('category_list')
        context['graph_sales_monthly'] = self.get_graph_sales_monthly()
        return context