from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from yandex_geocoder import Client

from shop_allhere import settings
from shop_allhere.utils import transliterate


SUBPAGESARTICLE_ADDRESS = "Enter a url address for article, otherwise the address will be set automatically"
SUBPAGESARTICLE_UNIQ_TEMPLATE = "check if the page will use a unique HTML template"
SHOPS_CITY = "Enter the city where the store is located"
SHOPS_ADDRESS = "Enter address of shop in the format City, street, house number"
SHOPS_LATITUDE = "indicates the latitude of the location on the world map"
SHOPS_LONGITUDE = "indicates the longitude of the location on the world map"


class SubPagesArticle(models.Model):
    title = models.CharField(max_length=40, help_text="Enter a titles article")
    address = models.CharField(max_length=40, help_text=SUBPAGESARTICLE_ADDRESS,
                               null=True, blank=True)
    section = models.ForeignKey('SubPagesSection', on_delete=models.SET_NULL,
                                related_name='content', null=True, blank=True)
    body = HTMLField(help_text="Enter a text article", null=True, blank=True)
    uniq_template = models.BooleanField(default=False, help_text=SUBPAGESARTICLE_UNIQ_TEMPLATE)

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse('app_shop:subpage_allhere_in_russia', args=[self.address])

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.address:
            self.address = transliterate(self.title)
        return super(SubPagesArticle, self).save()

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


class Shops(models.Model):
    name = models.CharField(max_length=40, help_text="Enter store name")
    city = models.CharField(max_length=20, help_text=SHOPS_CITY)
    address = models.CharField(max_length=100, help_text=SHOPS_ADDRESS)
    type = models.ForeignKey('ShopType', on_delete=models.SET_NULL, related_name='content',
                             null=True, blank=True)
    description = HTMLField(help_text="Enter a store description", null=True, blank=True)
    latitude = models.DecimalField(help_text=SHOPS_LATITUDE, max_digits=10, decimal_places=7,
                                   editable=False, null=True, blank=True)
    longitude = models.DecimalField(help_text=SHOPS_LONGITUDE, max_digits=10, decimal_places=7,
                                    editable=False, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app_shop:shop_detail', args=[self.id])

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        client = Client("%s" % settings.API_KEY_YANDEX_GEOCODER)
        coordinates = client.coordinates(self.address)
        self.latitude = coordinates[0]
        self.longitude = coordinates[1]
        return super(Shops, self).save()

    class Meta:
        ordering = ['city', 'type', 'name']
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'


class ShopType(models.Model):
    title = models.CharField(max_length=30, help_text="Enter a type of shop")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'ShopType'
        verbose_name_plural = 'ShopsType'


class News(models.Model):
    title = models.CharField(max_length=100, help_text="Enter a news titles")
    body = HTMLField(help_text="Enter a news text")
    datetime = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('allhere_in_russia:news', args=[self.id])

    class Meta:
        ordering = ['datetime', 'title']
        verbose_name = 'News'
        verbose_name_plural = 'News'
