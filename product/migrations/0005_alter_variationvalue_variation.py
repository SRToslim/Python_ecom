# Generated by Django 4.2.4 on 2023-09-08 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_variationvalue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variationvalue',
            name='variation',
            field=models.CharField(blank=True, choices=[('size', 'Size'), ('color', 'Color')], max_length=100, null=True),
        ),
    ]