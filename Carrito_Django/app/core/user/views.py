from django.conf.urls import url
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import Group
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.user.forms import UserForm, UserProfileForm
from core.user.models import User
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from django.urls import reverse_lazy


#Vista basade en Clase ListView
class UserListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    
    #Se Define Modelo.
    model = User
    
    #Se Define nombre del Template que contiene la lista.
    template_name = 'user/list.html'
    permission_required = 'view_user'
    url_redirect = reverse_lazy('dashboard')

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
                for i in User.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)
    
    #Modificación de la funcion get_context_data. Se genera variable "context". Se asignan nombres la lista para poder ser ocupadas en el template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List of Users' 
        context['create_url'] = reverse_lazy('create_user')
        context['list_url'] = reverse_lazy('user_list')
        context['entity'] = 'Users'
        context['dt_function'] = 'getUserData()'
        return context

class UserCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):

    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'add_user'
    url_redirect = reverse_lazy('user_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                print(form)
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['title'] = 'Create User'
        context['entity'] = 'Users' 
        context['list_url'] = reverse_lazy('user_list')
        context['action'] = 'add'
        context['url_create'] = '/users/create/'
        return context

class UserUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/edit.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'change_user'
    url_redirect = reverse_lazy('user_list')

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
        context['title'] = 'Update User' 
        context['create_url'] = reverse_lazy('create_user')
        context['list_url'] = reverse_lazy('user_list')
        context['entity'] = 'Users'
        context['action'] = 'edit'
        #context['url_edit'] = '/users/update/'
        return context

class UserDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'delete_user'
    url_redirect = reverse_lazy('user_list')

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
        context['title'] = 'Delete User' 
        context['create_url'] = reverse_lazy('create_user')
        context['list_url'] = reverse_lazy('user_list')
        context['entity'] = 'Users'
        context['action'] = 'delete'
        return context

class UserChangeGroup(LoginRequiredMixin,View):
    def get(self,request,*args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk = self.kwargs['pk'])
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('dashboard'))

class UserProfileView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'user/profile.html'
    success_url = '/erp/dashboard/'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset = None):
        return self.request.user

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
        context['title'] = 'Update Profile' 
        # context['create_url'] = reverse_lazy('create_user')
        # context['list_url'] = reverse_lazy('user_list')
        context['entity'] = 'Profile'
        context['action'] = 'edit'
        #context['url_edit'] = '/users/update/'
        context['form_submit'] = '/users/profile/'
        return context

class UserChangePasswordView(LoginRequiredMixin,FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class = None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder'] = 'Enter your actual password'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Enter your new password'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm your new password'
        return form
    

    def post(self, request, *args, **kwargs):
        data = {}
        print(self.success_url)
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request,form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change Password' 
        # context['create_url'] = reverse_lazy('create_user')
        # context['list_url'] = reverse_lazy('user_list')
        context['entity'] = 'Password'
        context['action'] = 'edit'
        #context['url_edit'] = '/users/update/'
        context['form_submit'] = '/users/change/password/'
        return context