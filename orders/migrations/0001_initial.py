# Generated by Django 5.1.5 on 2025-02-17 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hide', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'محافظة',
                'verbose_name_plural': 'محافظات',
            },
        ),
    ]
