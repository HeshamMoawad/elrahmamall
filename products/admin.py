from django.contrib import admin
from .models import Brand , Category
from .models import Product



class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', )
    search_fields = ('name', 'brand__name', 'categories__name')
    list_filter = ('brand', 'categories')


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)