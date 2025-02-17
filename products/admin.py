from django.contrib import admin

from products.views import brands
from .models import Brand , Category
from .models import Product


class BrandAdmin(admin.ModelAdmin):
    list_display = ('ar_name','ar_hide')
    search_fields = ('name',)

    @admin.display(description="الاسم",ordering="name")
    def ar_name(self, obj:Brand):
        return obj.name
    
    @admin.display(description="اخفاء",boolean=True,ordering="hide")
    def ar_hide(self, obj:Brand):
        return obj.hide
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('ar_name','ar_hide', "ar_is_sale" )
    search_fields = ('name',)

    @admin.display(description="الاسم",ordering="name")
    def ar_name(self, obj:Category):
        return obj.name
    
    @admin.display(description="اخفاء",boolean=True,ordering="hide")
    def ar_hide(self, obj:Category):
        return obj.hide
    
    @admin.display(description="تابع للعروض",boolean=True,ordering="is_sale")
    def ar_is_sale(self, obj:Category):
        return obj.is_sale


class ProductAdmin(admin.ModelAdmin):
    list_display = ('ar_name', 'ar_brand', 'ar_price','ar_hide' )
    search_fields = ('name', 'brand__name', 'categories__name')
    list_filter = ('brand', 'categories')

    @admin.display(description="الاسم",ordering="name")
    def ar_name(self, obj:Product):
        return obj.name
    
    @admin.display(description="العلامة التجارية",ordering="brand")
    def ar_brand(self, obj:Product):
        return obj.brand
    
    @admin.display(description="السعر",ordering="price")
    def ar_price(self, obj:Product):
        return obj.price
    
    @admin.display(description="اخفاء",boolean=True,ordering="hide")
    def ar_hide(self, obj:Product):
        return obj.hide

admin.site.register(Brand,BrandAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)