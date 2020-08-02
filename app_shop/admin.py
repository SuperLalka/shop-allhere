from django.contrib import admin

from .models import Shops, ShopType, SubPagesArticle, SubPagesSection


@admin.register(SubPagesArticle)
class SubPagesArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'uniq_template')
    list_filter = ('section', 'uniq_template')


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
