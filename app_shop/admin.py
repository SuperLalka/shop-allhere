from django.contrib import admin
from django.db import models
from django.forms import TextInput

from .models import News, Product, ProductClassification, Shops, ShopType, SubPagesArticle, SubPagesSection


@admin.register(SubPagesArticle)
class SubPagesArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'uniq_template')
    list_filter = ('section', 'uniq_template')
    search_fields = ['title']


@admin.register(SubPagesSection)
class SubPagesSectionAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Shops)
class ShopsAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'type')
    list_filter = ('type', 'city')


@admin.register(ShopType)
class ShopTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime'
    list_display = ('title', 'datetime')
    list_per_page = 50
    formfield_overrides = {models.CharField: {'widget': TextInput(attrs={'size': '100'})}}
    search_fields = ('title', 'body')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'classification')
    list_per_page = 50


@admin.register(ProductClassification)
class ProductClassificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)
