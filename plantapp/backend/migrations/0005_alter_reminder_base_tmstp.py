# Generated by Django 3.2 on 2021-06-01 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='base_tmstp',
            field=models.DateTimeField(),
        ),
    ]
