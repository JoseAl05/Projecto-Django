from core.erp.models import Product
from core.erp.forms import TestForm,TestForm2
from core.erp.models import Category
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView


class TestView(TemplateView):
    template_name = 'email.html'


 #Excepcion del token csrfmiddleware
    @method_decorator(csrf_exempt)
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #Modificación metodo Post
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searc_product_id':
                data = []
                for i in Product.objects.filter(cat_id = request.POST['id']):
                    data.append({'id':i.id,'name':i.name})
            elif action == 'autocomplete':
                data=[]
                for i in Category.objects.filter(name__icontains=request.POST['term']):
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
            #data = Category.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Selects anidados'
        context['form'] = TestForm()
        return context

class TestView2(TemplateView):
    template_name = 'test_select2.html'


 #Excepcion del token csrfmiddleware
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #Modificación metodo Post
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searc_product_id':
                data = [{'id':'','text':'-------------'}]
                for i in Product.objects.filter(cat_id = request.POST['id']):
                    data.append({'id':i.id,'text':i.name})
            elif action == 'autocomplete':
                data=[]
                for i in Category.objects.filter(name__icontains=request.POST['term']):
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
            #data = Category.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Selects anidados'
        context['form'] = TestForm2()
        return context
    