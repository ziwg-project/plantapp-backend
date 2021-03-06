# Generated by Django 3.2 on 2021-04-18 20:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plant',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='plant',
            name='text',
        ),
        migrations.AddField(
            model_name='plant',
            name='image_url',
            field=models.URLField(default='about:blank'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plant',
            name='name',
            field=models.CharField(default='template', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plant',
            name='sci_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('base_tmstp', models.TimeField()),
                ('intrvl_num', models.IntegerField()),
                ('intrvl_type', models.CharField(choices=[('S', 'SECONDS'), ('M', 'MINUTES'), ('H', 'HOURS'), ('D', 'DAYS'), ('W', 'WEEKS')], max_length=1)),
                ('plant_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.plant')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('O', 'OUTSIDE'), ('I', 'INSIDE')], max_length=1)),
                ('owner_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='plant',
            name='loc_fk',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='backend.location'),
            preserve_default=False,
        ),
    ]
