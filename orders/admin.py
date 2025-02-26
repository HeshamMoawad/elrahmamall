from django.contrib import admin
from .models import (
    Address ,
    Order ,
    Item ,
    PaymentAccountModel ,
    PaymentMethodModel ,
    Links
)
# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display = ('ar_name', 'ar_price', 'ar_hide')
    search_fields = ('name',)

    @admin.display(description="اسم المحافظة", ordering="name")
    def ar_name(self, obj: Address):
        return obj.name

    @admin.display(description="سعر التوصيل", ordering="price")
    def ar_price(self, obj: Address):
        return obj.price

    @admin.display(description="اخفاء", boolean=True, ordering="hide")
    def ar_hide(self, obj: Address):
        return obj.hide


admin.site.register(Address, AddressAdmin)


# OrderAdmin with Arabic display methods
class OrderAdmin(admin.ModelAdmin):
    list_display = ('ar_order_uuid', 'ar_user', 'ar_total_price','ar_is_cash_payment','ar_is_delivery_paid', 'ar_is_online_payment','ar_is_paid', 'ar_order_date')
    search_fields = ('order_uuid', 'user__username')

    @admin.display(description="رقم الطلب", ordering="order_uuid")
    def ar_order_uuid(self, obj: Order):
        return obj.order_uuid

    @admin.display(description="المستخدم", ordering="user")
    def ar_user(self, obj: Order):
        return obj.user

    @admin.display(description="السعر الإجمالي", ordering="total_price")
    def ar_total_price(self, obj: Order):
        return obj.total_price

    @admin.display(description="تاريخ الطلب", ordering="order_date")
    def ar_order_date(self, obj: Order):
        return obj.order_date

    @admin.display(description="الاوردر كاش", ordering="is_cash_payment" , boolean=True)
    def ar_is_cash_payment(self, obj: Order):
        return obj.is_cash_payment
    
    @admin.display(description="تم دفع التوصيل", ordering="is_delivery_paid" , boolean=True)
    def ar_is_delivery_paid(self, obj: Order):
        return obj.is_delivery_paid
    

    @admin.display(description="الدفع اونلاين", ordering="is_online_payment" , boolean=True)
    def ar_is_online_payment(self, obj: Order):
        return obj.is_online_payment
    

    @admin.display(description="تم دفع المبلغ كامل اونلاين", ordering="is_paid" , boolean=True)
    def ar_is_paid(self, obj: Order):
        return obj.is_paid
    

# ItemAdmin with Arabic display methods
class ItemAdmin(admin.ModelAdmin):
    # Since Item is related via ManyToMany to Order, this admin displays basic item details.
    list_display = ('ar_product', 'ar_quantity')
    search_fields = ('product__name',)

    @admin.display(description="المنتج", ordering="product__name")
    def ar_product(self, obj: Item):
        return obj.product.name if obj.product else "غير محدد"

    @admin.display(description="عدد المنتج", ordering="quantity")
    def ar_quantity(self, obj: Item):
        return obj.quantity


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PaymentAccountModel)
admin.site.register(PaymentMethodModel)
admin.site.register(Links)
