# Generated by Django 4.2.5 on 2023-10-01 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_alter_vendor_slug'),
        ('cart', '0030_alter_order_shipping_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(through='cart.OrderItem', to='product.product'),
        ),
    ]
