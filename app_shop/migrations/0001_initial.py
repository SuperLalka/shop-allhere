# Generated by Django 3.0.8 on 2020-07-28 11:11

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
                ('address', models.CharField(blank=True, max_length=30, null=True)),
                ('body', tinymce.models.HTMLField(help_text='Enter a text article')),
                ('title', models.CharField(help_text='Enter a titles article', max_length=100)),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='content', to='app_shop.SubPagesSection')),
            ],
            options={
                'verbose_name': 'SubPages Article',
                'verbose_name_plural': 'SubPages Articles',
            },
        ),
    ]