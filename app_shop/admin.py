from django import forms
from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.forms import TextInput

from app_shop.models import (
    Advertising, ClassificationFilters, FiltersForClassifications,
    OrderList, Product, ProductClassification, ProductListForOrder,
    ProductQuantity, Promotions, PromotionsForCategory
)
from allhere_in_russia.models import News, Shops, ShopType, SubPagesArticle, SubPagesSection
from shop_allhere.utils import ReadableJSONFormField


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
    formfield_overrides = {models.CharField: {'widget': TextInput(attrs={'size': '100'})}}
    list_display = ('title', 'datetime')
    list_per_page = 50
    search_fields = ('title', 'body')


class ProductCharacteristicsForm(forms.ModelForm):
    article = forms.IntegerField(label="Артикул товара", required=False)
    the_brand = forms.CharField(label="Бренд", max_length=50, required=False, widget=TextInput(attrs={'size': '50'}))
    calorie_content = forms.IntegerField(label="Калорийность", required=False)
    proteins = forms.FloatField(label="Белки на 100 г, г", required=False)
    fats = forms.FloatField(label="Жиры на 100 г, г", required=False)
    carbohydrates = forms.FloatField(label="Углеводы на 100 г, г", required=False)
    net_weight = forms.FloatField(label="Масса нетто, кг", required=False)
    gross_weight = forms.FloatField(label="Масса брутто, кг", required=False)
    ingredients = forms.CharField(
        label="Ингредиенты", max_length=150, required=False, widget=forms.Textarea(attrs={'rows': 3}))
    dimensions = forms.CharField(label="ДхШхВ, мм", max_length=10, required=False)
    manufacturer = forms.CharField(
        label="Производитель", max_length=100, required=False, widget=forms.Textarea(attrs={'rows': 2}))
    country_of_origin = forms.CharField(label="Страна производства", max_length=20, required=False)

    def save(self, *args, **kwargs):
        specifications = self.instance.specifications
        for key, value in self.cleaned_data.items():
            if key in self.declared_fields.keys() and value:
                specifications[self.fields[key].label] = value
        self.instance.specifications = specifications
        return super(ProductCharacteristicsForm, self).save(*args, **kwargs)


class ProductQuantityInline(admin.TabularInline):
    model = ProductQuantity


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductCharacteristicsForm
    formfield_overrides = {
        JSONField: {'form_class': ReadableJSONFormField},
    }
    inlines = [ProductQuantityInline]
    list_display = ('name', 'price', 'the_final_price', 'classification')
    list_per_page = 50
    search_fields = ('name',)


class ClassificationFiltersInline(admin.StackedInline):
    model = ClassificationFilters


@admin.register(ProductClassification)
class ProductClassificationAdmin(admin.ModelAdmin):
    inlines = [ClassificationFiltersInline]
    list_display = ('name', 'id', 'category', 'highest_category')
    search_fields = ('name',)


@admin.register(FiltersForClassifications)
class FiltersForClassificationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'priority')


class PromotionsForCategoryInline(admin.StackedInline):
    model = PromotionsForCategory


@admin.register(Promotions)
class PromotionsAdmin(admin.ModelAdmin):
    inlines = [PromotionsForCategoryInline]
    list_display = ('name', 'start_time', 'end_time', 'for_carousel', 'advertising')
    search_fields = ('name',)


@admin.register(Advertising)
class AdvertisingAdmin(admin.ModelAdmin):
    list_display = ('id', 'obligatory', 'idx_among_products', 'idx_among_promotions')


class ProductListForOrderInline(admin.TabularInline):
    model = ProductListForOrder


@admin.register(OrderList)
class OrderListAdmin(admin.ModelAdmin):
    date_hierarchy = 'order_creation_date'
    formfield_overrides = {models.CharField: {'widget': TextInput(attrs={'size': '100'})}}
    inlines = [ProductListForOrderInline]
    list_display = ('id', 'order_creation_date', 'address', 'cost')
    search_fields = ('address',)
