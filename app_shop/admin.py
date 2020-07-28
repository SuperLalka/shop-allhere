from django.contrib import admin
from .models import SubPagesArticle, SubPagesSection


@admin.register(SubPagesArticle)
class SubPagesArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'section')
    list_filter = ('title', 'section')


@admin.register(SubPagesSection)
class SubPagesSectionAdmin(admin.ModelAdmin):
    list_display = ('title',)
