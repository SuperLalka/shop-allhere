# Generated by Django 3.0.8 on 2020-08-18 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0002_promotions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promotions',
            options={'ordering': ('-end_time',), 'verbose_name': 'Promotion', 'verbose_name_plural': 'Promotions'},
        ),
    ]