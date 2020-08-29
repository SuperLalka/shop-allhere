from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from yandex_geocoder import Client

from app_shop.utils import transliterate
from shop_allhere import settings


class SubPagesArticle(models.Model):
    title = models.CharField(max_length=40, help_text="Enter a titles article")
    address = models.CharField(
        max_length=40, help_text="Enter a url address for article, otherwise the address will be set automatically",
        null=True, blank=True)
    section = models.ForeignKey(
        'SubPagesSection', on_delete=models.SET_NULL, related_name='content', null=True, blank=True)
    body = HTMLField(help_text="Enter a text article", null=True, blank=True)
    uniq_template = models.BooleanField(default=False, help_text="check if the page will use a unique HTML template")

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
    city = models.CharField(max_length=20, help_text="Enter the city where the store is located")
    address = models.CharField(
        max_length=100, help_text="Enter address of shop in the format City, street, house number")
    type = models.ForeignKey('ShopType', on_delete=models.SET_NULL, related_name='content', null=True, blank=True)
    description = HTMLField(help_text="Enter a store description", null=True, blank=True)
    latitude = models.DecimalField(help_text="indicates the latitude of the location on the world map",
                                   max_digits=10, decimal_places=7, editable=False, null=True, blank=True)
    longitude = models.DecimalField(help_text="indicates the longitude of the location on the world map",
                                    max_digits=10, decimal_places=7, editable=False, null=True, blank=True)

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


class SubscriptionEmails(models.Model):
    email = models.EmailField(max_length=40, help_text="Enter email for mailing", unique=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Mailing address'
        verbose_name_plural = 'Postal addresses'


class News(models.Model):
    title = models.CharField(max_length=100, help_text="Enter a news titles")
    body = HTMLField(help_text="Enter a news text")
    datetime = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('app_shop:news', args=[self.id])

    class Meta:
        ordering = ['datetime', 'title']
        verbose_name = 'News'
        verbose_name_plural = 'News'


DELIVERY_TERMS = (
        ('a', 'Мелкогабаритный товар'),
        ('b', 'Среднегабаритный товар'),
        ('c', 'Крупногабаритный товар'),
    )


class Product(models.Model):
    name = models.CharField(max_length=100, help_text="Enter product name")
    price = models.PositiveIntegerField(help_text="Enter product price")
    description = HTMLField(help_text="Enter a store description", null=True, blank=True)
    images = models.ImageField(upload_to="")
    discount = models.PositiveSmallIntegerField(
        default=None, help_text="If need, enter amount of discount", null=True, blank=True)
    classification = models.ForeignKey(
        'ProductClassification', on_delete=models.CASCADE, related_name='class_content', null=True, blank=True)
    specifications = JSONField(encoder={}, null=True, blank=True)
    slug = models.CharField(max_length=120, editable=False, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app_shop:product_detail', args=[self.slug])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = transliterate(self.name)
        return super(Product, self).save()

    class Meta:
        ordering = ('name',)


class ProductClassification(models.Model):
    category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, help_text="Enter а product category")
    highest_category = models.BooleanField(default=False)
    slug = models.CharField(max_length=120, editable=False, null=True, blank=True)

    def __str__(self):
        category = str(self.category).replace("/None", "")
        return '{0} /{1}'.format(self.name, category)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = transliterate(self.name)
        return super(ProductClassification, self).save()

    def get_child(self):
        return ProductClassification.objects.filter(category_id=self.id)

    def get_parent(self):
        path = [self]

        def recursive_get(item):
            if item.category:
                path.append(item.category)
                recursive_get(item.category)
            else:
                return path

        recursive_get(self)
        return list(reversed(path))

    class Meta:
        ordering = ('name', 'highest_category')


class Promotions(models.Model):
    name = models.CharField(max_length=100, help_text="Enter product name")
    description = HTMLField(help_text="Enter a store description", null=True, blank=True)
    images = models.ImageField(upload_to="promotions")
    start_time = models.DateField(
        help_text="Use an interactive calendar image or enter a date in the format 'YYYY-MM-DD'", null=True, blank=True)
    end_time = models.DateField(
        help_text="Use an interactive calendar image or enter a date in the format 'YYYY-MM-DD'", null=True, blank=True)
    for_carousel = models.BooleanField(
        help_text="Check, if promotion should be used for the main carousel", default=False)
    for_category = models.ManyToManyField(
        'ProductClassification', related_name='promo_class')

    def __str__(self):
        return '{0} ({1} - {2})'.format(self.name, self.start_time, self.end_time)

    def list_categories(self):
        return self.objects.for_category

    class Meta:
        ordering = ('-end_time',)
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'


class OrderList(models.Model):
    product_list = models.ManyToManyField('Product', through='ProductListForOrder')
    cost = models.PositiveSmallIntegerField()
    customer = models.CharField(max_length=20, help_text="Customer", null=True, blank=True)
    customer_phone = models.CharField(max_length=20, help_text="Customer phone", null=True, blank=True)
    address = models.CharField(max_length=100, help_text="Delivery address")
    order_creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} / {1}'.format(self.address, self.cost)


class ProductListForOrder(models.Model):
    orderlist = models.ForeignKey(OrderList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = "app_shop_productlistfororder"
