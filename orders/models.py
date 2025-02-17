from django.db import models

# Create your models here.

class Address(models.Model):
    name = models.CharField(verbose_name="اسم المحافظة",max_length=255)
    price = models.DecimalField(verbose_name="سعر التوصيل" ,max_digits=10, decimal_places=2)
    hide = models.BooleanField(verbose_name="اخفاء" ,default=False)
    class Meta:
        verbose_name = "محافظة"
        verbose_name_plural = "محافظات"

