# Generated by Django 4.2.4 on 2023-08-31 05:06

import autoslug.fields
import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='brand/')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='brand/banner/')),
                ('featured', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('disabled', 'Disabled'), ('published', 'Published')], default='published', max_length=10)),
                ('meta_title', models.CharField(blank=True, max_length=100, null=True)),
                ('meta_description', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='category/icon/')),
                ('image', models.ImageField(blank=True, null=True, upload_to='category/image/')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='category/banner/')),
                ('featured', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('disabled', 'Disabled'), ('published', 'Published')], default='published', max_length=10)),
                ('meta_title', models.CharField(blank=True, max_length=100, null=True)),
                ('meta_description', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True)),
                ('address', models.CharField(max_length=250, null=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('disabled', 'Disabled'), ('published', 'Published')], default='published', max_length=10)),
                ('gmap', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Location',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(blank=True, default=None, editable=False, null=True, populate_from='name', unique=True)),
                ('unit', models.CharField(choices=[('kg', 'kg'), ('pkt', 'pkt'), ('gm', 'gm'), ('bunch', 'bunch'), ('dozen', 'dozen'), ('liter', 'liter'), ('box', 'box'), ('piece', 'piece')], max_length=100)),
                ('pack_size', models.DecimalField(decimal_places=3, max_digits=5)),
                ('min_qty', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('type', models.CharField(choices=[('physical', 'Physical'), ('digital', 'Digital')], default='physical', max_length=10)),
                ('barcode', models.CharField(blank=True, default=None, max_length=30, null=True, unique=True)),
                ('image', models.ImageField(upload_to='products/')),
                ('hover_image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('old_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('discount', models.CharField(blank=True, choices=[('flat', 'Flat'), ('percent', 'Percent')], max_length=10, null=True)),
                ('tax', models.IntegerField(blank=True, default=5, null=True)),
                ('tax_type', models.CharField(choices=[('flat', 'Flat'), ('percent', 'Percent')], default='percent', max_length=10)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('qty', models.CharField(max_length=10)),
                ('sku', models.CharField(default=None, max_length=30, unique=True)),
                ('offer', models.CharField(blank=True, choices=[('today_deal', "Today's Deal"), ('Savings', 'Great Saving'), ('buy1get1', 'Buy 1 Get 1')], default=None, max_length=10, null=True)),
                ('cod', models.BooleanField(default=True, verbose_name='Cash on Delivery')),
                ('featured', models.BooleanField(default=False)),
                ('meta_title', models.CharField(blank=True, max_length=100, null=True)),
                ('meta_description', models.CharField(blank=True, max_length=250, null=True)),
                ('meta_image', models.ImageField(blank=True, null=True, upload_to='products/meta/')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('disabled', 'Disabled'), ('published', 'Published')], default='in_review', max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(default='product.jpg', upload_to='product-images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Gallery Images',
            },
        ),
        migrations.CreateModel(
            name='ProductVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(blank=True, choices=[('youtube', 'YouTube'), ('facebook', 'Facebook'), ('dailymotion', 'Dailymotion'), ('vimeo', 'Vimeo')], max_length=100, null=True)),
                ('link', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Product Video',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(blank=True, default=None, editable=False, null=True, populate_from='title', unique=True)),
                ('image', models.ImageField(default='default.png', upload_to='vendor/')),
                ('cover_image', models.ImageField(default='cover-photo.png', upload_to='vendor/')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('address', models.CharField(default='Mirpur, Dhaka', max_length=250)),
                ('contact', models.CharField(default='+8801966172000', max_length=100)),
                ('chat_resp_time', models.CharField(default='100', max_length=100)),
                ('shipping_on_time', models.CharField(default='100', max_length=100)),
                ('authentic_rating', models.CharField(default='100', max_length=100)),
                ('days_return', models.CharField(default='100', max_length=100)),
                ('warranty_period', models.CharField(default='100', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Vendors',
            },
        ),
    ]
