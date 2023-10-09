from django import forms
from django.forms import ModelForm

from cart.models import Order


class OrderForm(ModelForm):
    payment = forms.ChoiceField(widget=forms.CheckboxInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Order
        fields = '__all__'
