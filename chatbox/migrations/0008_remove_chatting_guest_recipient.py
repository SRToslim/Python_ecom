# Generated by Django 4.2.6 on 2023-10-05 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbox', '0007_chatting_guest_recipient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatting',
            name='guest_recipient',
        ),
    ]
