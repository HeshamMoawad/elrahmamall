from django import forms
from orders.models import Order, Item

class OrderForm(forms.ModelForm):
    # For the ManyToManyField, you might want to use a custom widget such as CheckboxSelectMultiple
    # items = forms.ModelMultipleChoiceField(
    #     queryset=Item.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False
    # )

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
            'raw_address',
            'is_cash_payment',
            'is_online_payment',
            'items',
            'total_price'
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
    
    