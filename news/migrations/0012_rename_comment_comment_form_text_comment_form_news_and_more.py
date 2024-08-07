# Generated by Django 4.2.6 on 2024-07-29 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0011_remove_comment_parent_alter_comment_news_reply'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment_form',
            old_name='comment',
            new_name='text',
        ),
        migrations.AddField(
            model_name='comment_form',
            name='news',
            field=models.ForeignKey(default='news', on_delete=django.db.models.deletion.CASCADE, to='news.news'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment_form',
            name='user',
            field=models.ForeignKey(default='user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reply',
            name='comment',
            field=models.ForeignKey(default='comment', on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='news.comment_form'),
            preserve_default=False,
        ),
    ]
