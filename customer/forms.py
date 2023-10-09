from django import forms

from customer.models import BillingAddress, ShippingAddress
from userauth.models import User
from userauth.models import Profile


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    membership_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    class Meta:
        model = User
        fields = ['email', 'username', 'phone']


class UpdateAdminForm(forms.ModelForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['phone']


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


class BillingAddressForm(forms.ModelForm):

    class Meta:
        model = BillingAddress
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'required': 'required'}),
            'lname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'billing_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'billing_address2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Town'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Postcode / ZIP'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'cname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional information'})
        }


class ShippingAddressForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'lname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'cname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'shipping_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'shipping_address2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State / County'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Town'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Postcode / ZIP'}),
        }
