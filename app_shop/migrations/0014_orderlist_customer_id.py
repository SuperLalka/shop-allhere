# Generated by Django 3.0.8 on 2020-08-31 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0013_auto_20200828_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlist',
            name='customer_id',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
