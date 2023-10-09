# Generated by Django 4.2.4 on 2023-09-14 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_billingaddress_billing_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='billing_address',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='city',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='country',
            field=models.CharField(choices=[('Bangladesh', 'Bangladesh')], max_length=15),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='fname',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='lname',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='phone',
            field=models.CharField(max_length=11),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='zipcode',
            field=models.CharField(max_length=5),
        ),
    ]
