# Generated by Django 3.0.8 on 2020-09-10 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0022_auto_20200910_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlist',
            name='cost',
            field=models.FloatField(),
        ),
    ]
