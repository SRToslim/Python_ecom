# Generated by Django 4.2.4 on 2023-09-08 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_productreview'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariationValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variation', models.CharField(blank=True, choices=[('size', 'size'), ('color', 'color')], max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('price', models.CharField(blank=True, max_length=5, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
