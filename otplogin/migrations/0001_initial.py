# Generated by Django 4.2.4 on 2023-09-07 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OTPProvidor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('providor', models.CharField(choices=[('SSLWireless', 'SSLWireless'), ('MIMSMS', 'MIMSMS'), ('Twilio', 'Twilio'), ('Firebase', 'Firebase')], max_length=12)),
                ('is_active', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
    ]
