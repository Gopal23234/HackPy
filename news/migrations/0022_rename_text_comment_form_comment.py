# Generated by Django 4.2.6 on 2024-07-29 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0021_rename_text_comment_form_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment_form',
            old_name='text',
            new_name='comment',
        ),
    ]
