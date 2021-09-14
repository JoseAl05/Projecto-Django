from django.db import models
from datetime import datetime

from django.db.models.deletion import CASCADE


class Type(models.Model):
    name = models.CharField(max_length=255,verbose_name='Nombre')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
        ordering = ['id']

class Category(models.Model):
        name = models.CharField(max_length=255,verbose_name='Nombre')

        def __str__(self):
            return self.name
    
        class Meta:
            verbose_name = 'Caregoria'
            verbose_name_plural = 'Categorias'
            ordering = ['id']


class Employee(models.Model):
    categ = models.ManyToManyField(Category)
    type = models.ForeignKey(Type,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,verbose_name='Nombre')
    dni = models.CharField(max_length=10,unique=True,verbose_name='DNI')
    date_joined = models.DateField(default=datetime.now(),verbose_name='Fecha de Registro')
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    age = models.PositiveIntegerField(default=0)
    salario = models.DecimalField(default=0.00,max_digits=9,decimal_places=2)
    state = models.BooleanField(default=True)
    gender = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to = 'avatar/%Y/%m/%d',null = True,blank = True)
    cv = models.FileField(upload_to = 'cv/%Y/%m/%d',null = True, blank = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        db_table = 'empleado'
        ordering = ['id']


