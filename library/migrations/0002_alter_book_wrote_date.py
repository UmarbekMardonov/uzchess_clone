# Generated by Django 5.0 on 2023-12-22 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='wrote_date',
            field=models.DateTimeField(),
        ),
    ]