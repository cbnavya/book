# Generated by Django 4.2 on 2023-11-11 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='bk_image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
