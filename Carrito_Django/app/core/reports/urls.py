from core.reports.views import ReportSaleView
from django.urls import path


urlpatterns = [

    #Reports
    path('sale/',ReportSaleView.as_view(),name='report_sale_view'),
]