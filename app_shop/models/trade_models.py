from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField

from shop_allhere.utils import transliterate


class Product(models.Model):
    name = models.CharField(max_length=100, help_text="Enter product name")
    price = models.PositiveIntegerField(help_text="Enter product price")
    description = HTMLField(help_text="Enter a store description", null=True, blank=True)
    images = models.ImageField(upload_to="products")
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
        app_label = 'app_shop'
        ordering = ('name',)


class ProductClassification(models.Model):
    category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, help_text="Enter а product category")
    highest_category = models.BooleanField(default=False)
    slug = models.CharField(max_length=120, editable=False, null=True, blank=True)
    filter = models.ManyToManyField('FiltersForClassifications', through='ClassificationFilters')

    def __str__(self):
        category = str(self.category).replace("/None", "")
        return '{0} /{1}'.format(self.name, category)

    def get_absolute_url(self):
        return reverse('app_shop:section_products', args=[self.id])

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
        app_label = 'app_shop'
        ordering = ('id', 'highest_category')


FILTER_TYPE = [
    ("TXT", "Фильтр по буквенному значению"),
    ("INT", "Фильтр по числовому значению (MIN и MAX)"),
    ("CSM", "Фильтр по чекбоксам из всех возможных значений поля"),
]


class FiltersForClassifications(models.Model):
    name = models.CharField(max_length=30, help_text="Enter а product category")
    type = models.CharField(max_length=3, choices=FILTER_TYPE, help_text="Enter а filter type")
    slug = models.CharField(max_length=40, editable=False, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = transliterate(self.name)
        return super(FiltersForClassifications, self).save()

    class Meta:
        app_label = 'app_shop'


class ClassificationFilters(models.Model):
    classification = models.ForeignKey(ProductClassification, on_delete=models.CASCADE)
    filter = models.ForeignKey(FiltersForClassifications, on_delete=models.CASCADE)

    class Meta:
        app_label = 'app_shop'
        db_table = "app_shop_classificationfilters"


class OrderList(models.Model):
    product_list = models.ManyToManyField('Product', through='ProductListForOrder')
    cost = models.PositiveSmallIntegerField()
    customer = models.CharField(max_length=20, help_text="Customer", null=True, blank=True)
    customer_id = models.PositiveSmallIntegerField(null=True, blank=True)
    customer_phone = models.CharField(max_length=20, help_text="Customer phone", null=True, blank=True)
    address = models.CharField(max_length=100, help_text="Delivery address")
    order_creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} / {1}'.format(self.address, self.cost)

    def get_products_in_list(self):
        return ProductListForOrder.objects.filter(orderlist_id=self.id)

    class Meta:
        app_label = 'app_shop'


class ProductListForOrder(models.Model):
    orderlist = models.ForeignKey(OrderList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        app_label = 'app_shop'
        db_table = "app_shop_productlistfororder"
