# Generated by Django 3.2.7 on 2021-09-26 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0002_category_desc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='cate',
        ),
        migrations.AddField(
            model_name='product',
            name='cat',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='erp.category', verbose_name='Categoría'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product/%Y/%m/%d', verbose_name='Imagen'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pvp',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Precio de Venta'),
        ),
    ]
