from datetime import datetime

from django.shortcuts import get_object_or_404

from product.models import Category, Location, Brand
from shop_settings.models import Header, News, Footer, Currency, Slider


def default(request):
    day = datetime.now().date()
    categories = Category.objects.filter(status='published')[:7]
    brands = Brand.objects.filter(status='published')
    locations = Location.objects.all()

    headers = get_object_or_404(Header)
    flash_news = News.objects.all()
    foot = get_object_or_404(Footer)
    currencies = Currency.objects.filter(is_active=True)
    sliders = Slider.objects.filter(active=True)

    return {
        'day': day,
        'categories': categories,
        'locations': locations,
        'brands': brands,
        'headers': headers,
        'flash_news': flash_news,
        'foot': foot,
        'currencies': currencies,
        'sliders': sliders,
    }
