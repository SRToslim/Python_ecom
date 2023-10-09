from django import forms
from django.forms import ModelForm

from product.models import Category, STATUS, Brand, ProductImages, Product, Unit, TYPE, Tax_Type, Offer, Discount_Type


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['slug']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Category Name', 'style': 'background:transparent'}),
            'icon': forms.FileInput(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'banner': forms.FileInput(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'featured': forms.NullBooleanSelect(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'status': forms.Select(choices=STATUS, attrs={'class': 'form-control', 'style': 'background:transparent'}),
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'
        exclude = ['slug']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Brand Name', 'style': 'background:transparent'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'banner': forms.FileInput(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'featured': forms.NullBooleanSelect(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'status': forms.Select(choices=STATUS, attrs={'class': 'form-control', 'placeholder': 'Full Name',
                                                          'style': 'background:transparent'}),
        }


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['slug']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Product Name', 'style': 'background:transparent'}),
            'category': forms.Select(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'brand': forms.Select(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'vendor': forms.Select(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'location': forms.Select(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'unit': forms.Select(choices=Unit, attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'pack_size': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': '0.00', 'style': 'background:transparent'}),
            'min_qty': forms.NumberInput(
                attrs={'class': 'form-control', 'value': '1', 'style': 'background:transparent'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'product_type': forms.Select(choices=TYPE,
                                         attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'barcode': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Product Barcode', 'style': 'background:transparent'}),
            'image': forms.FileInput(
                attrs={'class': 'form-control', 'style': 'background:transparent', 'id': 'img-input'}),
            'hover_image': forms.FileInput(
                attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'price': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '0.00', 'style': 'background:transparent'}),
            'old_price': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '0.00', 'style': 'background:transparent'}),
            'discount': forms.Select(choices=Discount_Type, attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'tax': forms.NumberInput(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'tax_type': forms.Select(attrs={'class': 'form-control', 'style': 'background:transparent'},
                                     choices=Tax_Type),
            'qty': forms.NumberInput(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'sku': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'SKU', 'style': 'background:transparent'}),
            'offer': forms.Select(choices=Offer, attrs={'class': 'form-control', 'placeholder': 'Full Name',
                                                        'style': 'background:transparent'}),
            'cod': forms.NullBooleanSelect(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'featured': forms.NullBooleanSelect(attrs={'class': 'form-control', 'style': 'background:transparent'}),
            'status': forms.Select(choices=STATUS, attrs={'class': 'form-control', 'placeholder': 'Full Name',
                                                          'style': 'background:transparent'}),
        }


class ProductImageForm(ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), required=False)

    class Meta:
        model = ProductImages
        fields = '__all__'
