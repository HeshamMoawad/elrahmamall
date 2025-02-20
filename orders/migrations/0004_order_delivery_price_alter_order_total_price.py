# Generated by Django 5.1.5 on 2025-02-20 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_item_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='سعر التوصيل'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=25, verbose_name='السعر الإجمالي'),
        ),
    ]
