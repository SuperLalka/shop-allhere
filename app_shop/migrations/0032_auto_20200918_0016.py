# Generated by Django 3.0.8 on 2020-09-17 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0031_promotions_obligatory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productclassification',
            options={'ordering': ['id', 'highest_category']},
        ),
        migrations.AlterModelTable(
            name='orderlist',
            table=None,
        ),
    ]
