# Generated by Django 4.2.6 on 2023-10-09 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='qty',
            field=models.PositiveIntegerField(),
        ),
    ]