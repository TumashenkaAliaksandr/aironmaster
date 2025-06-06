# Generated by Django 5.2.1 on 2025-05-28 16:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_about_alter_footerinfo_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='OurService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название сервиса')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='service_photos/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Наш сервис',
                'verbose_name_plural': 'Наши сервисы',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='itemobject',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='webapp.ourservice', verbose_name='Сервис'),
        ),
    ]
