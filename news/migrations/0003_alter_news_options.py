# Generated by Django 5.0 on 2024-01-05 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_news_content_en_news_content_uz_news_title_en_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'News', 'verbose_name_plural': 'News'},
        ),
    ]
