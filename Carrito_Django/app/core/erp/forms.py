from django.db.models.base import Model
from django.forms import *
from core.erp.models import Category,Product
from bootstrap_modal_forms.forms import BSModalModelForm

class CategoryForm(ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True


    class Meta:
        model=Category
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder':'Ingrese su Nombre',
                }
            ),
            'desc': Textarea(
                attrs={
                    'placeholder':'Ingrese descripción de la categoría',
                    'rows': 3,
                    'cols': 3
                }
            )
        }  

    def save(self, commit=True):
        data={}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error']=form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


    #Se obtiene el objeto del formulario. Se pueden hacer validaciones (Tamaño del campo, etc.)
    def clean(self):
        cleaned = super().clean()
        if len(cleaned['name']) <=  5:
            raise forms.ValidationError('Validacion')
        print(cleaned)
        return cleaned

class ProductForm(ModelForm):


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True


    class Meta:
        model=Product
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder':'Ingrese su Nombre',
                }
            ),
        }  

    def save(self, commit=True):
        data={}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error']=form.errors
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

class TestForm(Form):
    categories = ModelChoiceField(queryset=Category.objects.all(),widget=Select(attrs={
        'class' : 'form-control'
    }))

    products = ModelChoiceField(queryset=Product.objects.none(),widget=Select(attrs={
        'class' : 'form-control'
    }))