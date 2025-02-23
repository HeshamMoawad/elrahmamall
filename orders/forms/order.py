from django import forms
from orders.models import Order, Item

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'user',
            'country',
            'district',
            'apartment',
            'street',
            'building',
            'floor',
            'note',
            'raw_address',
            'is_cash_payment',
            'is_online_payment',
            'total_price' ,
            'delivery_price'
        ]
    def clean(self):
        cleaned_data = super().clean()
        is_cash_payment = cleaned_data.get("is_cash_payment")
        is_online_payment = cleaned_data.get("is_online_payment")
        # Example: ensure that one and only one payment method is chosen.
        if is_cash_payment and is_online_payment:
            self.add_error('is_cash_payment', "Select only one payment method")
        if not is_cash_payment and not is_online_payment:
            self.add_error('is_cash_payment', "Select a payment method")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Customize raw_address by combining several address fields
        if not instance.raw_address :
            address_components = [
                instance.apartment,
                instance.building,
                instance.street,
                instance.district,
                instance.country.name if instance.country else ""
            ]
            instance.raw_address = ", ".join(filter(None, address_components))
        if commit:
            instance.save()
            self.save_m2m()
        return instance
    
class ItemsForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "order",
            "product",
            "quantity"
        ]
