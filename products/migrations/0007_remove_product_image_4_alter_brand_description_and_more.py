# Generated by Django 5.1.5 on 2025-02-17 22:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_brand_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_4',
        ),
        migrations.AlterField(
            model_name='brand',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='الوصف'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='hide',
            field=models.BooleanField(default=False, verbose_name='اخفاء'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='brands/', verbose_name='الصورة'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=255, verbose_name='الاسم'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='الوصف'),
        ),
        migrations.AlterField(
            model_name='category',
            name='hide',
            field=models.BooleanField(default=False, verbose_name='اخفاء'),
        ),
        migrations.AlterField(
            model_name='category',
            name='is_sale',
            field=models.BooleanField(default=False, verbose_name='تابع للعروض'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, verbose_name='الاسم'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.brand', verbose_name='العلامة التجارية'),
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(to='products.category', verbose_name='التصنيفات'),
        ),
        migrations.AlterField(
            model_name='product',
            name='count',
            field=models.IntegerField(verbose_name='العدد الحالى'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='الوصف'),
        ),
        migrations.AlterField(
            model_name='product',
            name='details',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='التفاصيل'),
        ),
        migrations.AlterField(
            model_name='product',
            name='hide',
            field=models.BooleanField(default=False, verbose_name='اخفاء'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_1',
            field=models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='الصورة الرئيسية'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_2',
            field=models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='الصورة 2'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_3',
            field=models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='الصورة 3'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='الاسم'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='السعر'),
        ),
    ]
