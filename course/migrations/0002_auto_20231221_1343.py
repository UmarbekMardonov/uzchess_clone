# Generated by Django 3.2.10 on 2023-12-21 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursebig',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='coursebig',
            name='title',
            field=models.CharField(blank=True, max_length=220, null=True),
        ),
    ]
