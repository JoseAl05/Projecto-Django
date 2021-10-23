import smtplib
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.views.generic.base import RedirectView
from app import settings
from core.login.forms import ResetPasswordForm, ChangePasswordForm
from core.user.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string

# Create your views here.


class LoginFormView(LoginView):
    template_name = 'login/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.NAME_VIEW_LOGIN_REDIRECT)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[' title'] = 'Login'
        return context


class LoginFormView2(FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy(settings.NAME_VIEW_LOGIN_REDIRECT)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['entity'] = 'Categories'
        context['list_url'] = reverse_lazy('category_list')
        return context


class LogoutRedirectView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


class ResetPasswordView(FormView):
    form_class = ResetPasswordForm
    template_name = 'login/reset_pwd.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def send_email_reset_password(self,user):
        data = {}
        try:
            url = settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']


            user.token = uuid.uuid4()
            user.save()


            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(settings.EMAIL_HOST_USER,
                             settings.EMAIL_HOST_PASSWORD)

            email_to = user.email

            msj = MIMEMultipart()
            msj['From'] = settings.EMAIL_HOST_USER
            msj['To'] = email_to
            msj['Subject'] = 'Reset Password'

            content = render_to_string('login/send_email.html',{
                'user' : user,
                'link_resetpwd':'http://{}/login/change/password/{}/'.format(url,str(user.token)),
                'link_home':'http://{}'.format(url)
            })
            msj.attach(MIMEText(content, 'html'))

            mailServer.sendmail(settings.EMAIL_HOST_USER, email_to, msj.as_string())
            
        except Exception as e:
            data['error'] = str(e)
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ResetPasswordForm(request.POST)  # self.get_form()
            if form.is_valid():
                user = form.get_user()
                data = self.send_email_reset_password(user)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reset Password'
        return context

class ChangePasswordView(FormView):
    form_class = ChangePasswordForm
    template_name = 'login/change_pwd.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self,request,*args, **kwargs):
        token = self.kwargs['token']
        print(token)
        if User.objects.filter(token = token):
            return super().get(request,*args, **kwargs)
        return HttpResponseRedirect('/')


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ChangePasswordForm(request.POST) 
            if form.is_valid():
                user = User.objects.get(token=self.kwargs['token'])
                user.set_password(request.POST['password'])
                user.token = uuid.uuid4()
                user.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change Password'
        context['user_token'] = self.kwargs['token']
        return context
