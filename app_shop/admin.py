from django.contrib import admin
from django.db import models
from django import forms
from django.forms import TextInput

from .models import News, Promotions, Product, ProductClassification, Shops, ShopType, SubPagesArticle, SubPagesSection


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


class ProductCharacteristicsForm(forms.ModelForm):
    article = forms.IntegerField(label="Артикул товара", required=False)
    the_brand = forms.CharField(label="Бренд", max_length=50, required=False, widget=TextInput(attrs={'size': '50'}))
    calorie_content = forms.IntegerField(label="Калорийность", required=False)
    proteins = forms.FloatField(label="Белки на 100 г.", required=False)
    fats = forms.FloatField(label="Жиры на 100 г.", required=False)
    carbohydrates = forms.FloatField(label="Углеводы на 100 г.", required=False)
    net_weight = forms.FloatField(label="Масса нетто, кг", required=False)
    gross_weight = forms.FloatField(label="Масса брутто, кг", required=False)
    ingredients = forms.CharField(
        label="Ингредиенты", max_length=150, required=False, widget=forms.Textarea(attrs={'rows': 3}))
    dimensions = forms.CharField(label="ДхШхВ, мм", max_length=10, required=False)
    manufacturer = forms.CharField(
        label="Производитель", max_length=100, required=False, widget=forms.Textarea(attrs={'rows': 2}))
    country_of_origin = forms.CharField(label="Страна производства", max_length=20, required=False)

    def save(self, *args, **kwargs):
        specifications = {}
        for key, value in self.cleaned_data.items():
            if key in self.declared_fields.keys() and value:
                specifications[self.fields[key].label] = value
        self.instance.specifications = specifications
        return super(ProductCharacteristicsForm, self).save(*args, **kwargs)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'classification')
    list_per_page = 50
    form = ProductCharacteristicsForm


@admin.register(ProductClassification)
class ProductClassificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)


@admin.register(Promotions)
class PromotionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'for_carousel', )
    search_fields = ('name',)
