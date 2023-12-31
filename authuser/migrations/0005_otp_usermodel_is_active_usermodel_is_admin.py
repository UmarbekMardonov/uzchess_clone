# Generated by Django 5.0 on 2024-01-05 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0004_usermodel_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.CharField(max_length=32)),
                ('code', models.CharField(max_length=64)),
                ('active_till', models.DateTimeField(editable=False)),
            ],
        ),
        migrations.AddField(
            model_name='usermodel',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
