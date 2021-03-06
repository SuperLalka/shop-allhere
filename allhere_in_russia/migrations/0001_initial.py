# Generated by Django 3.0.8 on 2020-09-01 11:17

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter a news titles', max_length=100)),
                ('body', tinymce.models.HTMLField(help_text='Enter a news text')),
                ('datetime', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
                'ordering': ['datetime', 'title'],
            },
        ),
        migrations.CreateModel(
            name='ShopType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter a type of shop', max_length=30)),
            ],
            options={
                'verbose_name': 'ShopType',
                'verbose_name_plural': 'ShopsType',
            },
        ),
        migrations.CreateModel(
            name='SubPagesSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter a sections of articles', max_length=30)),
            ],
            options={
                'verbose_name': 'SubPages Section',
                'verbose_name_plural': 'SubPages Sections',
            },
        ),
        migrations.CreateModel(
            name='SubPagesArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter a titles article', max_length=40)),
                ('address', models.CharField(blank=True, help_text='Enter a url address for article, otherwise the address will be set automatically', max_length=40, null=True)),
                ('body', tinymce.models.HTMLField(blank=True, help_text='Enter a text article', null=True)),
                ('uniq_template', models.BooleanField(default=False, help_text='check if the page will use a unique HTML template')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='content', to='allhere_in_russia.SubPagesSection')),
            ],
            options={
                'verbose_name': 'SubPages Article',
                'verbose_name_plural': 'SubPages Articles',
            },
        ),
        migrations.CreateModel(
            name='Shops',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter store name', max_length=40)),
                ('city', models.CharField(help_text='Enter the city where the store is located', max_length=20)),
                ('address', models.CharField(help_text='Enter address of shop in the format City, street, house number', max_length=100)),
                ('description', tinymce.models.HTMLField(blank=True, help_text='Enter a store description', null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, editable=False, help_text='indicates the latitude of the location on the world map', max_digits=10, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, editable=False, help_text='indicates the longitude of the location on the world map', max_digits=10, null=True)),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='content', to='allhere_in_russia.ShopType')),
            ],
            options={
                'verbose_name': 'Shop',
                'verbose_name_plural': 'Shops',
                'ordering': ['city', 'type', 'name'],
            },
        ),
    ]
