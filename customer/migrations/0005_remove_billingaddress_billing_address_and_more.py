# Generated by Django 4.2.4 on 2023-09-14 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_alter_shippingaddress_zipcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='billing_address',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='billing_address2',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='city',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='cname',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='country',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='email',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='lname',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='note',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='zipcode',
        ),
    ]
