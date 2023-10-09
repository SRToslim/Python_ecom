import codecs
import csv
import decimal
import os
from urllib.parse import urlparse

import requests
from _decimal import Decimal
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from dashboard.decorator import dashboard_access_required
from dashboard.utils import USER_TYPE_DEVELOPER, USER_TYPE_ADMIN
from product.forms import CSVUploadForm, ProductForm, ProductImageForm
from product.models import Product, Vendor, Category, Brand, Location, ProductImages
from userauth.models import User


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def product_list(request):
    products = Product.objects.all()
    item_per_page = 20
    paginator = Paginator(products, item_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'admin/product/index.html', {'page': page})


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def add_product(request):
    if request.method == 'post' or request.method == 'POST':
        files = request.FILES.getlist('images')
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()

            for file in files:
                ProductImages.objects.create(product=product, images=file)

        messages.success(request, 'Product successfully added.')
        return redirect('product_list')
    else:
        form = ProductForm()
        image = ProductImageForm()
    return render(request, 'admin/product/create.html', {'form': form, 'image': image})


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def edit_product(request, slug):
    if request.method == 'post' or request.method == 'POST':
        product = Product.objects.get(slug=slug)
        form = ProductForm(request.POST, request.FILES, instance=product)
        files = request.FILES.getlist('images')
        if form.is_valid():
            product = form.save(commit=False)
            product.save()

            for file in files:
                ProductImages.objects.create(product=product, images=file)

            messages.success(request, 'Product successfully updated.')
            return redirect(to='product_list')
    else:
        product = Product.objects.get(slug=slug)
        form = ProductForm(instance=product)
        image = ProductImageForm(instance=product)

        return render(request, 'admin/product/edit.html', {'product': product, 'form': form, 'image': image})


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def delete_product(request, slug):
    user = request.user
    if user.user_type in [USER_TYPE_DEVELOPER, USER_TYPE_ADMIN]:
        product = Product.objects.get(slug=slug)
        if product.image:
            os.remove(product.image.path)
            os.remove(product.hover_image.path)
        if product.gallery:
            os.remove(product.images.path)
        product.delete()
        messages.success(request, 'Product Deleted Successfully.')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request, 'Please contact Admin to delete this category.')
        return redirect(request.META.get('HTTP_REFERER'))


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def bulk_product_upload(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            if csv_file.name.endswith('.csv'):
                ifile = codecs.iterdecode(csv_file, 'latin-1')
                read = csv.reader(ifile)

                for row in read:
                    title, category, brand, vendor, location, unit, pack_size, min_qty, tags, product_type, barcode, \
                        image, hover_image, price, old_price, discount, tax, tax_type, description, qty, sku, offer, \
                        cod, featured, status = row

                    try:
                        user_instance, _ = User.objects.get_or_create(username=vendor)
                        vendor, _ = Vendor.objects.get_or_create(user=user_instance, title=vendor)
                        pack_size = Decimal(pack_size) if pack_size else None
                        min_qty = Decimal(min_qty) if min_qty else None
                        tax = int(tax) if tax else None
                        qty = int(qty) if qty else None
                    except decimal.InvalidOperation:
                        pack_size = 1
                        min_qty = 1
                        tax = 0
                        qty = 5

                    category, _ = Category.objects.get_or_create(title=category)
                    brand, _ = Brand.objects.get_or_create(title=brand)
                    location, _ = Location.objects.get_or_create(title=location)
                    product, _ = Product.objects.update_or_create(
                        barcode=barcode,
                        defaults={
                            'title': title,
                            'category': category,
                            'brand': brand,
                            'vendor': vendor,
                            'location': location,
                            'unit': unit,
                            'pack_size': pack_size,
                            'min_qty': min_qty,
                            'tags': tags,
                            'product_type': product_type,
                            'price': price,
                            'old_price': old_price if old_price else None,
                            'discount': discount,
                            'tax': tax,
                            'tax_type': tax_type,
                            'description': description,
                            'qty': qty,
                            'sku': sku,
                            'offer': offer,
                            'cod': bool(cod),
                            'featured': bool(featured),
                            'status': status,
                        }
                    )
                    product.save()

                    if image:
                        parsed_url = urlparse(image)
                        if parsed_url.scheme and parsed_url.netloc:
                            try:
                                new_image_data = requests.get(image).content
                                if product.image:
                                    product.image.delete()
                                product.image.save(os.path.basename(parsed_url.path), ContentFile(new_image_data),
                                                   save=True)
                            except Exception as e:
                                print(f"Error fetching or saving image from URL: {str(e)}")

                    if hover_image:
                        parsed_url = urlparse(hover_image)
                        if parsed_url.scheme and parsed_url.netloc:
                            try:
                                new_hover_image_data = requests.get(hover_image).content
                                if product.hover_image:
                                    product.hover_image.delete()
                                product.hover_image.save(os.path.basename(parsed_url.path),
                                                         ContentFile(new_hover_image_data), save=True)
                            except Exception as e:
                                print(f"Error fetching or saving image from URL: {str(e)}")
            return redirect('product_list')
    else:
        form = CSVUploadForm()

    return render(request, 'admin/product/bulk-upload.html', {'form': form})