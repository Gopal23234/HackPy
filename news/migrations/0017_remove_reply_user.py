# Generated by Django 4.2.6 on 2024-07-29 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0016_reply_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reply',
            name='user',
        ),
    ]
