# Generated by Django 3.2 on 2021-04-19 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20210418_2007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plant',
            name='image_url',
        ),
        migrations.AddField(
            model_name='plant',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
