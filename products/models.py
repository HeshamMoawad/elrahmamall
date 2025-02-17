from django.db import models 


class Category(models.Model):
    name = models.CharField(verbose_name="الاسم",max_length=255)
    description = models.TextField(verbose_name="الوصف",blank=True, null=True)
    is_sale = models.BooleanField(verbose_name="تابع للعروض",default=False)
    hide = models.BooleanField(verbose_name="اخفاء",default=False)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name ="تصنيف"
        verbose_name_plural = "التصنيفات"

class Brand(models.Model):
    name = models.CharField(verbose_name="الاسم",max_length=255)
    description = models.TextField(verbose_name="الوصف",blank=True, null=True)
    image = models.ImageField(verbose_name="الصورة",upload_to='brands/', blank=True, null=True)
    hide = models.BooleanField(verbose_name="اخفاء",default=False)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "علامة تجارية"
        verbose_name_plural = "العلامات التجارية"

class Product(models.Model):
    name = models.CharField(verbose_name="الاسم",max_length=255)
    description = models.TextField(verbose_name="الوصف",blank=True, null=True)
    price = models.DecimalField(verbose_name="السعر",max_digits=10, decimal_places=2)
    image_1 = models.ImageField(verbose_name="الصورة الرئيسية",upload_to='products/', blank=True, null=True)
    image_2 = models.ImageField(verbose_name="الصورة 2",upload_to='products/', blank=True, null=True)
    image_3 = models.ImageField(verbose_name="الصورة 3",upload_to='products/', blank=True, null=True)
    # image_4 = models.ImageField(verbose_name="",upload_to='products/', blank=True, null=True)
    categories = models.ManyToManyField(Category,verbose_name="التصنيفات")
    brand = models.ForeignKey(Brand,verbose_name="العلامة التجارية", on_delete=models.SET_NULL, null=True, blank=True)
    count = models.IntegerField(verbose_name="العدد الحالى",)
    details = models.TextField(verbose_name="التفاصيل",max_length=2000, blank=True, null=True)
    hide = models.BooleanField(verbose_name="اخفاء",default=False)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name ="منتج"
        verbose_name_plural = "المنتجات"
