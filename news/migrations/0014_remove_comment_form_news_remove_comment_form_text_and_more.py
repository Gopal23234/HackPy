# Generated by Django 4.2.6 on 2024-07-29 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_comment_form_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment_form',
            name='news',
        ),
        migrations.RemoveField(
            model_name='comment_form',
            name='text',
        ),
        migrations.RemoveField(
            model_name='comment_form',
            name='user',
        ),
        migrations.RemoveField(
            model_name='reply',
            name='comment',
        ),
    ]
