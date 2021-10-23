from django.contrib.auth.mixins import LoginRequiredMixin
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.mixins import isSuperUserMixin
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from core.erp.models import Client
from core.erp.forms import ClientForm
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from django.urls import reverse_lazy

class ClientListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):


    #Se Define Modelo.
    model = Client

    #Se Define nombre del Template que contiene la lista.
    template_name = 'client/list.html'

    permission_required = 'view_client'
    url_redirect = reverse_lazy('dashboard')

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
            if action == 'searchdata':
                data = []
                for i in Client.objects.all():
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
        context['title'] = 'List of Clients' 
        context['create_url'] = reverse_lazy('create_client')
        context['list_url'] = reverse_lazy('client_list')
        context['entity'] = 'Clients'
        context['dt_function'] = 'getClientData()'
        print(context)
        return context

class ClientCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('client_list')
    permission_required = 'add_client'
    url_redirect = reverse_lazy('client_list')

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
        context['title'] = 'Create Client'
        context['entity'] = 'Clients' 
        context['list_url'] = reverse_lazy('client_list')
        context['action'] = 'add'
        context['url_create'] = '/erp/client/create/'
        return context

class ClientUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/edit.html'
    success_url = reverse_lazy('client_list')
    permission_required = 'change_client'
    url_redirect = reverse_lazy('client_list')

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
        context['title'] = 'Update Client' 
        context['create_url'] = reverse_lazy('create_client')
        context['list_url'] = reverse_lazy('client_list')
        context['entity'] = 'Clients'
        context['action'] = 'edit'
        context['url_edit'] = '/erp/client/update/'
        return context

class ClientDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Client
    template_name = 'client/delete.html'
    success_url = reverse_lazy('client_list')
    permission_required = 'delete_client'
    url_redirect = reverse_lazy('client_list')

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
        context['title'] = 'Delete Client' 
        context['create_url'] = reverse_lazy('create_client')
        context['list_url'] = reverse_lazy('client_list')
        context['entity'] = 'Clients'
        context['action'] = 'delete'
        return context