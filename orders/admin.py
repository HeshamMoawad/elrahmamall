from django.contrib import admin
from .models import (
    Address
)
# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display = ('ar_name', 'ar_price', 'ar_hide')
    search_fields = ('name',)

    @admin.display(description="اسم المحافظة",ordering="name")
    def ar_name(self, obj:Address):
        return obj.name
    
    @admin.display(description="سعر التوصيل",ordering="price")
    def ar_price(self, obj:Address):
        return obj.price
    
    @admin.display(description="اخفاء",boolean=True,ordering="hide")
    def ar_hide(self, obj:Address):
        return obj.hide



admin.site.register(Address,AddressAdmin)
