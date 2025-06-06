# Generated by Django 5.2.1 on 2025-06-01 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0018_itemobject_description_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemobject',
            name='is_prokladki_mtgr',
            field=models.BooleanField(default=False, verbose_name='Прокладки'),
        ),
        migrations.AlterField(
            model_name='bannerpage',
            name='category',
            field=models.CharField(blank=True, choices=[('metal_structures', 'Металлоконструкции'), ('procladki', 'Прокладки'), ('steps_and_stairs', 'Ступеньки и Лестницы'), ('grills', 'Мангалы'), ('decor_elements', 'Элементы декора')], max_length=50, null=True, unique=True, verbose_name='Категория'),
        ),
    ]
