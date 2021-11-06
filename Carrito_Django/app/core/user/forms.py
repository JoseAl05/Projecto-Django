from datetime import date, datetime
from django.db.models.base import Model
from django.forms.fields import DecimalField
from django.forms import *
from core.user.models import User
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class UserForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'first_name','last_name','email','username','password','image','groups'
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder':'Enter your first name'
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder':'Enter your last name'
                }
            ),
            'email': TextInput(
                attrs={
                    'placeholder':'Enter your email'
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder':'Enter your username',
                }
            ),
            'password': PasswordInput(
                render_value=True,
                attrs={
                    'placeholder':'Enter your password',
                }
            ),
            'groups': SelectMultiple(
                attrs={
                    'class' :'select2',
                    'multiple':'multiple'
                }
            )
        }
        exclude = ['user_permissions','last_login','date_joined','is_superuser','is_active','is_staff']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                password = self.cleaned_data['password']


                form_user = form.save(commit=False)
                if form_user.pk is None:
                    form_user.set_password(password)
                else:
                    user = User.objects.get(pk=form_user.pk)
                    if user.password != password:
                        form_user.set_password(password)
                form_user.save()
                form_user.groups.clear()
                for g in self.cleaned_data['groups']:
                    form_user.groups.add(g)
                print(self.cleaned_data)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # Se obtiene el objeto del formulario. Se pueden hacer validaciones (Tamaño del campo, etc.)

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 5:
    #         raise forms.ValidationError('Validacion')
    #     print(cleaned)
    #     return cleaned

class UserProfileForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'first_name','last_name','email','username','password','image'
        widgets = {
            'first_name': TextInput(
                attrs={
                    'placeholder':'Enter your first name'
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder':'Enter your last name'
                }
            ),
            'email': TextInput(
                attrs={
                    'placeholder':'Enter your email'
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder':'Enter your username',
                }
            ),
            'password': PasswordInput(
                render_value=True,
                attrs={
                    'placeholder':'Enter your password',
                }
            ),
        }
        exclude = ['user_permissions','last_login','date_joined','is_superuser','is_active','is_staff','groups']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                password = self.cleaned_data['password']


                form_user = form.save(commit=False)
                if form_user.pk is None:
                    form_user.set_password(password)
                else:
                    user = User.objects.get(pk=form_user.pk)
                    if user.password != password:
                        form_user.set_password(password)
                form_user.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data