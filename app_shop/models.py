from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField


class SubPagesArticle(models.Model):
    title = models.CharField(max_length=100, help_text="Enter a titles article")
    address = models.CharField(max_length=30, help_text="Enter a url address for article")
    section = models.ForeignKey('SubPagesSection', on_delete=models.SET_NULL, related_name='content', null=True, blank=True)
    body = HTMLField(help_text="Enter a text article")

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse('app_shop:subpage_allhere_in_russia', args=[self.address])

    class Meta:
        verbose_name = 'SubPages Article'
        verbose_name_plural = 'SubPages Articles'


class SubPagesSection(models.Model):
    title = models.CharField(max_length=30, help_text="Enter a sections of articles")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'SubPages Section'
        verbose_name_plural = 'SubPages Sections'
