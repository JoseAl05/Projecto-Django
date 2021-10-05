from datetime import date, datetime
from django.db.models.base import Model
from django.forms import *
from core.erp.models import Category, Product, Client, Sale
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class CategoryForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese su Nombre',
                }
            ),
            'desc': Textarea(
                attrs={
                    'placeholder': 'Ingrese descripción de la categoría',
                    'rows': 3,
                    'cols': 3
                }
            )
        }
        exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # Se obtiene el objeto del formulario. Se pueden hacer validaciones (Tamaño del campo, etc.)

    def clean(self):
        cleaned = super().clean()
        if len(cleaned['name']) <= 5:
            raise forms.ValidationError('Validacion')
        print(cleaned)
        return cleaned


class ProductForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese su Nombre',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # #Se obtiene el objeto del formulario. Se pueden hacer validaciones (Tamaño del campo, etc.)
    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <=  5:
    #         raise forms.ValidationError('Validacion')
    #     print(cleaned)
    #     return cleaned


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Enter your Names',
                }
            ),
            'surnames': TextInput(
                attrs={
                    'placeholder': 'Enter your surnames',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Enter your dni'
                }
            ),
            'birthday': DateInput(
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d')
                }
            ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Enter your address'
                }
            ),
            'gender': Select()
        }
        exclude = ['user_creation', 'user_updated']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli': Select(attrs={
                'class': 'select2'
            }),
            'date_joined': DatePicker(
                options={
                    'maxDate': datetime.now().strftime('%Y-%m-%d'),
                    'useCurrent': True,
                    'collapse':False,
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            ),
            'subtotal': NumberInput(
                attrs={
                    'disabled' : True
                }
            ),
            'total': NumberInput(
                attrs={
                    'disabled': True
                }
            )
        }
        exclude = ['user_creation', 'user_updated']

    # def save(self, commit=True):
    #     data = {}
    #     form = super()
    #     try:
    #         if form.is_valid():
    #             form.save()
    #         else:
    #             data['error'] = form.errors
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return data


class TestForm(Form):
    categories = ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
        'class': 'form-control'
    }))

    products = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control'
    }))

    search = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter a description'
    }))


class TestForm2(Form):
    categories = ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
        'class': 'form-control select2'
    }))

    products = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2'
    }))

    search = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
        'class': 'form-control select2'
    }))
