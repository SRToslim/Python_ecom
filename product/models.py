from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.safestring import mark_safe
from taggit.managers import TaggableManager

from userauth.backend import User

STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('published', 'Published'),
)

Offer = (
    ('today_deal', "Today's Deal"),
    ('Savings', 'Great Saving'),
    ('buy1get1', 'Buy 1 Get 1')
)

TYPE = (
    ('physical', 'Physical'),
    ('digital', 'Digital'),
)

PROVIDER = (
    ('youtube', 'YouTube'),
    ('facebook', 'Facebook'),
    ('dailymotion', 'Dailymotion'),
    ('vimeo', 'Vimeo'),
)

Discount_Type = (
    ('flat', 'Flat'),
    ('percent', 'Percent'),
)

Tax_Type = (
    ('flat', 'Flat'),
    ('percent', 'Percent')
)

Unit = (
    ('kg', 'kg'),
    ('pkt', 'pkt'),
    ('gm', 'gm'),
    ('bunch', 'bunch'),
    ('dozen', 'dozen'),
    ('liter', 'liter'),
    ('box', 'box'),
    ('piece', 'piece'),
)


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, null=False, blank=False)
    slug = AutoSlugField(populate_from='title', unique=True)
    icon = models.ImageField(upload_to="category/icon/", blank=True, null=True)
    image = models.ImageField(upload_to="category/image/", blank=True, null=True)
    banner = models.ImageField(upload_to="category/banner/", blank=True, null=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS, max_length=10, default='published')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50">' % self.icon.url)

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    image = models.ImageField(upload_to="brand/", blank=True, null=True)
    banner = models.ImageField(upload_to="brand/banner/", blank=True, null=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS, max_length=10, default='published')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Brands'

    def brand_image(self):
        return mark_safe('<img src="%s" width="100" height="50">' % self.image.url)

    def __str__(self):
        return self.title


class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='title', null=True, blank=True, unique=True)
    image = models.ImageField(upload_to='vendor/', default='default.png')
    cover_image = models.ImageField(upload_to='vendor/', default='cover-photo.png')
    description = RichTextUploadingField(null=True, blank=True)
    address = models.CharField(max_length=250, default='Mirpur, Dhaka')
    contact = models.CharField(max_length=100, default='+8801966172000')
    chat_resp_time = models.CharField(max_length=100, default='100')
    shipping_on_time = models.CharField(max_length=100, default='100')
    authentic_rating = models.CharField(max_length=100, default='100')
    days_return = models.CharField(max_length=100, default='100')
    warranty_period = models.CharField(max_length=100, default='100')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="120" height="30">' % self.image.url)

    def __str__(self):
        return self.title


class Location(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    address = models.CharField(max_length=250, null=True)
    status = models.CharField(choices=STATUS, max_length=10, default='published')
    gmap = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Location"

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    slug = AutoSlugField(populate_from='name')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, related_name='brand')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, blank=True, null=True, related_name='vendor')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='location')
    unit = models.CharField(max_length=100, blank=False, null=False, choices=Unit)
    pack_size = models.DecimalField(max_digits=5, decimal_places=3)
    min_qty = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tags = TaggableManager()
    product_type = models.CharField(choices=TYPE, max_length=10, default='physical')
    barcode = models.CharField(unique=True, max_length=30, blank=True, null=True, default=None)
    image = models.ImageField(upload_to="products/", blank=False, null=False)
    hover_image = models.ImageField(upload_to="products/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.CharField(choices=Discount_Type, max_length=10, blank=True, null=True)
    tax = models.IntegerField(blank=True, null=True, default=5)
    tax_type = models.CharField(choices=Tax_Type, max_length=10, default='percent')
    description = RichTextUploadingField(null=True, blank=True)
    qty = models.PositiveIntegerField()
    sku = models.CharField(unique=True, max_length=30, blank=False, null=False, default=None)
    offer = models.CharField(choices=Offer, max_length=10, default=None, null=True, blank=True)
    cod = models.BooleanField(default=True, verbose_name='Cash on Delivery', null=True, blank=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS, max_length=10, default='in_review')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50">' % self.image.url)

    def __str__(self):
        return self.name

    def tax_price(self):
        if self.tax == 0 or None:
            tax_price = 0
            return tax_price
        else:
            tax_price = (self.price * self.tax / 100)
            return tax_price

    def current_price(self):
        present_price = (self.price + self.tax_price())
        return present_price

    def previous_price(self):
        pre_price = (self.old_price + self.tax_price())
        return pre_price

    def sale_price(self):
        if self.discount == 'flat':
            if self.old_price:
                new_price = (self.old_price - self.price)
                return new_price
        else:
            if self.old_price:
                new_price = ((self.old_price - self.price) / self.old_price) * 100
                return new_price

    def product_availability(self):
        if self.qty > 2:
            qty = '<span class="stock-status in-stock mb-0"> Available </span>'
        elif 2 >= self.qty > 0:
            qty = '<span class="stock-status low-stock mb-0"> Low Stock </span>'
        else:
            qty = '<span class="stock-status out-stock mb-0"> Out of Stock </span>'
        return mark_safe(qty)


class ProductImages(models.Model):
    images = models.ImageField(upload_to='product-images/', default='product.jpg')
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Gallery Images"


class ProductVideo(models.Model):
    product = models.ForeignKey(Product, related_name='video', on_delete=models.SET_NULL, null=True)
    provider = models.CharField(choices=PROVIDER, max_length=100, null=True, blank=True)
    link = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Video"


class ProductReview(models.Model):
    RATING = (
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.name

    def get_rating(self):
        return self.rating


class VariationManager(models.Manager):
    def sizes(self):
        return super(VariationManager, self).filter(variation='size')

    def colors(self):
        return super(VariationManager, self).filter(variation='color')


VARIATIONS_TYPE = (
    ('size', 'size'),
    ('color', 'color'),
)


class VariationValue(models.Model):
    variation = models.CharField(max_length=100, choices=VARIATIONS_TYPE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    price = models.CharField(max_length=5, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return self.name