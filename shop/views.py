import requests
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from ipware import get_client_ip
from taggit.models import Tag

from product.models import Category, Product, ProductReview, Brand, Vendor, Location
from shop.forms import ProductReviewForm
from shop.models import Visitor
from shop_settings.models import Banner
from userauth.utils import get_client_os_info, get_client_browser_info, get_client_device_info


def index_view(request):
    products = Product.objects.filter(status='published').order_by('-created_at')
    new_product = products[:15]
    recent_products = products[:3]
    banners = Banner.objects.filter(is_active=True)[:3]
    featured_cat = Category.objects.filter(featured=True)
    return render(request, 'home/index.html', {
        'products': products,
        'new_product': new_product,
        'recent_products': recent_products,
        'banners': banners,
        'featured_cat': featured_cat,
    })


def shop(request):
    products = Product.objects.filter(status='published').order_by('-created_at')

    item_per_page = 20
    paginator = Paginator(products, item_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'home/shop.html', {'page': page})


def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug, status='published')
    related_products = Product.objects.filter(category=product.category).exclude(slug=slug)[:4].select_related(
        'category')

    reviews = product.reviews.order_by('-date').prefetch_related('user')
    p_image = product.gallery.all()

    average_rating = reviews.aggregate(rating=Avg('rating'))

    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        make_review = not ProductReview.objects.filter(user=request.user, product=product).exists()

    context = {
        'p': product,
        'make_review': make_review,
        'p_image': p_image,
        'review_form': review_form,
        'average_rating': average_rating['rating'] if average_rating['rating'] else None,
        'reviews': reviews,
        'related_products': related_products,
    }

    return render(request, 'home/product-details.html', context)


def ajax_add_review(request, slug):
    product = Product.objects.get(slug=slug)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating'],
    )

    context = {
        'user': user.username,
        'fullName': user.profile.full_name,
        'image': user.profile.image.url,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_reviews': average_reviews
        }
    )


def category_list_view(request):
    category = Category.objects.all()
    return render(request, 'home/category.html', {'category': category})


def category_product_list_view(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(status='published', category=category)

    item_per_page = 20
    paginator = Paginator(products, item_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'category': category,
        'page': page
    }

    return render(request, 'home/category-product-list.html', context)


def vendor_list_view(request):
    vendors = Vendor.objects.all().annotate(product_count=Count('vendor'))

    context = {
        'vendors': vendors,
    }

    return render(request, 'home/vendor.html', context)


def vendor_details_view(request, slug):
    vendor = Vendor.objects.get(slug=slug)
    products = Product.objects.filter(status='published', vendor=vendor)

    item_per_page = 20
    paginator = Paginator(products, item_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'vendor': vendor,
        'page': page,
    }

    return render(request, 'home/vendor-details.html', context)


def brand_list_view(request):
    return render(request, 'home/brand.html')


def brand_product_list_view(request, slug):
    brand = Brand.objects.get(slug=slug)
    products = Product.objects.filter(status='published', brand=brand)

    item_per_page = 20
    paginator = Paginator(products, item_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'brand': brand,
        'page': page,
    }

    return render(request, 'home/brand-product-list.html', context)


def tag_list(request, tag_slug=None):
    products = Product.objects.filter(status='published').order_by('-created_at')

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    item_per_page = 20
    paginator = Paginator(products, item_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'tag': tag
    }

    return render(request, 'home/tag.html', context)


def location_product_list_view(request, slug):
    location = Location.objects.get(slug=slug)
    products = Product.objects.filter(status='published', location=location)

    item_per_page = 20
    paginator = Paginator(products, item_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'location': location,
        'page': page,
    }

    return render(request, 'location-product-list.html', context)


def search_view(request):
    query = request.GET.get('q')

    products = Product.objects.filter(name__icontains=query).order_by('-created_at')

    # product_names = [product.name for product in products]

    context = {
        'products': products,
        'query': query,
    }

    return render(request, 'home/search.html', context)
    # return JsonResponse(context)


def deals(request):
    products = Product.objects.filter(status='published')

    item_per_page = 20
    paginator = Paginator(products, item_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'home/deals.html', {'page': page})


def get_visitor_location(request):
    client_ip, _ = get_client_ip(request)

    if client_ip:
        api_key = 'd76c739332e04e1ca87bc4c926d5d1cb'
        api_url = f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={client_ip}"
        response = requests.get(api_url)
        if response.status_code == 200:
            client_os_info = get_client_os_info(request)
            client_browser_info = get_client_browser_info(request)
            client_device_info = get_client_device_info(request)
            location_data = response.json()
            city = location_data.get('city', 'Unknown')
            region = location_data.get('state_prov', 'Unknown')
            district = location_data.get('district', 'Unknown')
            zipcode = location_data.get('zipcode', 'Unknown')
            country = location_data.get('country_name', 'Unknown')

            visitor, _ = Visitor.objects.get_or_create(ip_address=client_ip, os_info=client_os_info,
                                                       browser_info=client_browser_info,
                                                       device_info=client_device_info, city=city, region=region,
                                                       country=country,
                                                       district=district, zipcode=zipcode)

    return redirect(request.META.get('HTTP_REFERER'))
