from django.db import models
from products.models import Product
from users.models import ElRahmaUser
from uuid import uuid4



class Address(models.Model):
    name = models.CharField(verbose_name="اسم المحافظة",max_length=255)
    price = models.DecimalField(verbose_name="سعر التوصيل" ,max_digits=10, decimal_places=2)
    hide = models.BooleanField(verbose_name="اخفاء" ,default=False)
    class Meta:
        verbose_name = "محافظة"
        verbose_name_plural = "محافظات"
    def __str__(self):
        return f"{self.name}"


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True, verbose_name="المنتج")
    quantity = models.IntegerField(verbose_name="عدد المنتج")

    def __str__(self):
        return f"{self.product.name} - {self.quantity} - {self.product.price * self.quantity}"



class Order(models.Model):
    user = models.ForeignKey(ElRahmaUser, on_delete=models.SET_NULL,null=True, verbose_name="المستخدم")
    country = models.ForeignKey(Address, on_delete=models.SET_NULL,null=True, verbose_name="المحافظة")
    district = models.CharField(verbose_name="الحى", max_length=255)
    apartment = models.CharField(verbose_name="الشقة", max_length=255)
    street = models.CharField(verbose_name="الشارع", max_length=255)
    building = models.CharField(verbose_name="المبنى", max_length=255)
    floor = models.CharField(verbose_name="الدور", max_length=255)
    raw_address = models.CharField(verbose_name="العنوان كامل كتابة", max_length=255)

    is_cash_payment = models.BooleanField(default=False, verbose_name="الدفع كاش")
    
    is_online_payment = models.BooleanField(default=True, verbose_name="الدفع اونلاين")
    
    is_delivery_paid = models.BooleanField(default=False, verbose_name="تم دفع التوصيل")

    is_paid = models.BooleanField(default=False, verbose_name="مدفوع")

    items = models.ManyToManyField(Item,verbose_name="المنتجات")


    order_uuid= models.UUIDField(verbose_name="ID الاوردر",max_length= 250 , default=uuid4 , editable=False)
    total_price = models.DecimalField(max_digits=25, decimal_places=2, verbose_name="السعر الإجمالي")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0, verbose_name="سعر التوصيل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if all([self.is_cash_payment,self.is_online_payment]):
            raise ValueError("Can't add two types of payments")
        elif not any([self.is_cash_payment,self.is_online_payment]):
            raise ValueError("Must Chose any type of payments")
        
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "طلب"
        verbose_name_plural = "طلبات"




def reduce_items(sender, instance:Item, created:bool, **kwargs):
    if created :
        print(sender, instance, created, kwargs)
        product = instance.product
        product.count -= instance.quantity
        product.save()



# models.signals.post_save.connect(reduce_items, sender=Order)
models.signals.post_save.connect(reduce_items, sender=Item)
