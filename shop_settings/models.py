from django.db import models
from django.utils.safestring import mark_safe


class Currency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Currency'

    def __str__(self):
        return self.name


class Header(models.Model):
    logo = models.ImageField(upload_to='logo/', default='assets/imgs/theme/logo.svg')
    contact = models.CharField(max_length=15, default='01773030088')

    class Meta:
        verbose_name_plural = "Header Settings"

    def image(self):
        return mark_safe('<img src="%s" width="120" height="30">' % self.logo.url)


class News(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Flash News"


class Footer(models.Model):
    about = models.CharField(max_length=1000, default='A Complete Store For Your Family')
    address = models.CharField(max_length=1000, default='30/2, 30/3 SHAHJADPUR, PRAGATI SARANI, Dhaka 1212')
    email = models.EmailField(max_length=100, default='support@helpbazar.com')
    time = models.CharField(max_length=255, blank=True, null=True)
    android = models.CharField(max_length=1000, blank=True, null=True)
    iphone = models.CharField(max_length=1000, blank=True, null=True)
    payment = models.ImageField(upload_to='payment/', default='payment-method.png')
    mobile = models.CharField(max_length=15, default='01966172000')
    working = models.CharField(max_length=100, default='Working 9:00 - 16:00')
    support_title = models.CharField(max_length=100, default='24/7 Support Center')
    facebook = models.CharField(max_length=255, default='facebook.com')
    instagram = models.CharField(max_length=255, default='instagram.com')
    twitter = models.CharField(max_length=255, default='twitter.com')
    youtube = models.CharField(max_length=255, default='youtube.com')
    linkedin = models.CharField(max_length=255, default='linkedin.com')
    flash_news = models.CharField(max_length=100, default='Up to 15% discount on your first subscribe')

    class Meta:
        verbose_name_plural = "Footer Settings"


class Slider(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    sliders = models.ImageField(upload_to='slider/')
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Sliders'

    def slider(self):
        return mark_safe('<img src="%s" width="120" height="40">' % self.sliders.url)


class Banner(models.Model):
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banner/')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Banners'

    def banner(self):
        return mark_safe('<img src="%s" width="120" height="40">' % self.image.url)


class Order_value(models.Model):
    min_order = models.IntegerField(null=True, blank=True)