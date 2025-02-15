from django.db import models 


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_sale = models.BooleanField(default=False)
    hide = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='brands/', blank=True, null=True)
    hide = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_1 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='products/', blank=True, null=True)
    categories = models.ManyToManyField(Category)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    count = models.IntegerField()
    details = models.TextField(max_length=2000, blank=True, null=True)
    hide = models.BooleanField(default=False)

    def __str__(self):
        return self.name