# Generated by Django 4.2.4 on 2023-09-14 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0024_remove_shippingaddress_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
    ]
