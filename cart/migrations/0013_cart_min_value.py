# Generated by Django 4.2.4 on 2023-09-08 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_remove_cart_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='min_value',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]