# Generated by Django 3.0.8 on 2020-09-18 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0034_auto_20200918_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertising',
            name='promotion',
        ),
        migrations.AddField(
            model_name='promotions',
            name='advertising',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promo', to='app_shop.Advertising'),
        ),
        migrations.AlterField(
            model_name='advertising',
            name='idx_among_products',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Specify a position for fixing a advertising in the list of products (0 - ∞)', null=True),
        ),
        migrations.AlterField(
            model_name='advertising',
            name='idx_among_promotions',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Specify a position for fixing a advertising in a block of promotions (0 - 4)', null=True),
        ),
    ]