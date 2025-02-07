from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
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
    categories = models.ManyToManyField(Category)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    count = models.IntegerField()
    details = models.TextField(max_length=2000, blank=True, null=True)
    hide = models.BooleanField(default=False)

    def __str__(self):
        return self.name