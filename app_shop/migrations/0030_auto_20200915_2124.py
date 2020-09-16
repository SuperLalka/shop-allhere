# Generated by Django 3.0.8 on 2020-09-15 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0029_auto_20200915_1425'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='promotions',
            options={'ordering': ['-end_time'], 'verbose_name': 'Promotion', 'verbose_name_plural': 'Promotions'},
        ),
        migrations.AlterField(
            model_name='visitstatistics',
            name='actions',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterModelTable(
            name='orderlist',
            table='app_shop_orderlist',
        ),
    ]