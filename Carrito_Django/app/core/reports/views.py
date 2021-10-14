from django.db.models.fields import DecimalField
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from core.erp.models import Sale
from core.reports.forms import ReportForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt 
from django.db.models.functions import Coalesce
from django.db.models import Sum, Value as V
from decimal import Decimal

class ReportSaleView(TemplateView):
    template_name = 'sale/report.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                search = Sale.objects.all()
                print(search)
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date,end_date])
                    print(search)
                for i in search:
                    data.append([
                        i.id,
                        i.cli.names,
                        i.date_joined.strftime('%Y-%m-%d'),
                        format(i.subtotal,'.2f'),
                        format(i.iva,'.2f'),
                        format(i.total,'.2f')
                    ])
                
                subtotal = search.aggregate(sum_subtotal=Coalesce(Sum('subtotal'),V(0),output_field=DecimalField()))
                iva = search.aggregate(sum_iva=Coalesce(Sum('iva'),V(0),output_field=DecimalField()))
                total = search.aggregate(sum_total=Coalesce(Sum('total'),V(0),output_field=DecimalField()))

                data.append([
                    '---',
                    '---',
                    '---',
                    subtotal['sum_subtotal'],
                    iva['sum_iva'],
                    total['sum_total']
                    # format(iva, '.2f'),
                    # format(total, '.2f'),
                ])
            else:
                data['error'] = 'Error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sale Reports' 
        context['dt_function'] = 'generate_report()'
        context['form'] = ReportForm
        return context
    