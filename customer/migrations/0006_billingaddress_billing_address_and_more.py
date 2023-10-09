# Generated by Django 4.2.4 on 2023-09-14 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_remove_billingaddress_billing_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='billing_address',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='billing_address2',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='city',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='cname',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='country',
            field=models.CharField(blank=True, choices=[('Bangladesh', 'Bangladesh')], max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='lname',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='zipcode',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='fname',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
