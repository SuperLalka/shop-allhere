from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField

from allhere_in_russia.models import Shops
from shop_allhere.utils import transliterate


PRODUCT_DISCOUNT = "Enter the discount percentage for this product"
PRODUCT_DISCOUNT_FIXED_PRICE = "Enter the price of the fixed discount"
PROMOTIONS_TIME = "Use an interactive calendar image or enter a date in the format 'YYYY-MM-DD'"
PROMOTIONS_FOR_CAROUSEL = "Check, if promotion should be used for the main carousel"


class Product(models.Model):
    name = models.CharField(max_length=100, help_text="Enter product name")
    price = models.FloatField(help_text="Enter product price")
    the_final_price = models.FloatField(editable=False, null=True, blank=True)
    description = HTMLField(help_text="Enter a store description", null=True, blank=True)
    images = models.ImageField(upload_to="products")
    discount = models.PositiveSmallIntegerField(default=None, help_text=PRODUCT_DISCOUNT,
                                                null=True, blank=True)
    discount_fixed_price = models.FloatField(help_text=PRODUCT_DISCOUNT_FIXED_PRICE,
                                             null=True, blank=True)
    classification = models.ForeignKey('ProductClassification', on_delete=models.CASCADE,
                                       related_name='class_content', null=True, blank=True)
    specifications = JSONField(encoder={}, null=True, blank=True)
    slug = models.CharField(max_length=120, editable=False, null=True, blank=True)
    quantity = models.ManyToManyField(Shops, through='ProductQuantity')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app_shop:product_detail', args=[self.slug])

    def get_current_prices(self):
        if self.discount_fixed_price:
            return self.discount_fixed_price
        elif self.discount:
            return round(self.price - (self.price / self.discount), 2)
        else:
            if not self.classification:
                return self.price

            def check_discount(item):
                discount = (PromotionsForCategory.objects.filter(
                    category_id=item.id)).values_list('discount', flat=True)
                if discount:
                    self.the_final_price = round(self.price - (self.price / discount.first()), 2)
                    return self.the_final_price
                elif item.category:
                    return check_discount(item.category)
                return self.price

            return check_discount(self.classification)

    def get_current_discount(self):
        if self.discount_fixed_price:
            return 'старая цена - {0}'.format(self.price)
        elif self.discount:
            return str(self.discount) + "%"
        else:
            if not self.classification:
                return self.price

            def check_discount(item):
                the_final_price = None
                discount = (PromotionsForCategory.objects.filter(
                    category_id=item.id)).values_list('discount', flat=True)
                if discount:
                    the_final_price = str(discount.first()) + "%"
                    return the_final_price
                elif item.category:
                    return check_discount(item.category)
                return the_final_price

            return check_discount(self.classification)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.the_final_price = self.get_current_prices()
        if not self.slug:
            self.slug = transliterate(self.name)
        return super(Product, self).save()

    class Meta:
        app_label = 'app_shop'
        ordering = ['name']


class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'app_shop'
        db_table = "app_shop_productquantity"


class ProductClassification(models.Model):
    category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, help_text="Enter а product category")
    highest_category = models.BooleanField(default=False)
    slug = models.CharField(max_length=120, editable=False, null=True, blank=True)
    filter = models.ManyToManyField('FiltersForClassifications', through='ClassificationFilters')

    def __str__(self):
        category = str(self.category).replace("/None", "")
        return '{0} /{1}'.format(self.name, category)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = transliterate(self.name)
        return super(ProductClassification, self).save()

    def get_absolute_url(self):
        return reverse('app_shop:section_products', args=[self.id])

    def get_child(self):
        return ProductClassification.objects.filter(category_id=self.id)

    def get_current_discount(self):
        if PromotionsForCategory.objects.filter(category_id=self.id).exists():
            return str((PromotionsForCategory.objects.get(category_id=self.id)).discount) + "%"

    def get_parent(self):

        def recursive_get(item):
            yield item
            if item.category:
                yield from recursive_get(item.category)

        path = reversed(list(recursive_get(self)))
        return path

    class Meta:
        app_label = 'app_shop'
        ordering = ('id', 'highest_category')


FILTER_TYPE = [
    ("TXT", "Фильтр по буквенному значению"),
    ("INT", "Фильтр по числовому значению (MIN и MAX)"),
    ("CSM", "Фильтр по чекбоксам из всех возможных значений поля"),
]


class FiltersForClassifications(models.Model):
    name = models.CharField(max_length=30, help_text="Enter а filter name")
    type = models.CharField(max_length=3, choices=FILTER_TYPE, help_text="Enter а filter type")
    priority = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'app_shop'
        ordering = ['priority']


class ClassificationFilters(models.Model):
    classification = models.ForeignKey(ProductClassification, on_delete=models.CASCADE)
    filter = models.ForeignKey(FiltersForClassifications, on_delete=models.CASCADE)

    class Meta:
        app_label = 'app_shop'
        db_table = "app_shop_classificationfilters"


class Promotions(models.Model):
    name = models.CharField(max_length=100, help_text="Enter product name")
    description = HTMLField(help_text="Enter a store description", null=True, blank=True)
    images = models.ImageField(upload_to="promotions")
    start_time = models.DateField(help_text=PROMOTIONS_TIME, null=True, blank=True)
    end_time = models.DateField(help_text=PROMOTIONS_TIME, null=True, blank=True)
    for_carousel = models.BooleanField(help_text=PROMOTIONS_FOR_CAROUSEL, default=False)
    for_category = models.ManyToManyField('ProductClassification', through='PromotionsForCategory')

    def __str__(self):
        return '{0} ({1} - {2})'.format(self.name, self.start_time, self.end_time)

    class Meta:
        app_label = 'app_shop'
        ordering = ['-end_time']
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'


class PromotionsForCategory(models.Model):
    promotion = models.ForeignKey('Promotions', on_delete=models.CASCADE)
    category = models.ForeignKey('ProductClassification', on_delete=models.CASCADE)
    discount = models.PositiveSmallIntegerField()

    class Meta:
        app_label = 'app_shop'
        db_table = "app_shop_promotionsforcategory"


class OrderList(models.Model):
    product_list = models.ManyToManyField('Product', through='ProductListForOrder')
    cost = models.FloatField()
    customer = models.CharField(max_length=20, help_text="Customer", null=True, blank=True)
    customer_id = models.PositiveSmallIntegerField(null=True, blank=True)
    customer_phone = models.CharField(max_length=20, help_text="Customer phone", null=True, blank=True)
    address = models.CharField(max_length=100, help_text="Delivery address")
    order_creation_date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False, help_text="Notes whether the order has been paid")

    def __str__(self):
        return '{0} / {1}'.format(self.address, self.cost)

    def get_products_in_list(self):
        return ProductListForOrder.objects.filter(orderlist_id=self.id)

    class Meta:
        app_label = 'app_shop'
        db_table = "app_shop_orderlist"


class ProductListForOrder(models.Model):
    orderlist = models.ForeignKey(OrderList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.PositiveSmallIntegerField(null=True, blank=True)
    count = models.PositiveSmallIntegerField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        write_off_product = ProductQuantity.objects.get(shop_id=self.store, product=self.product)
        write_off_product.number = write_off_product.number - self.count
        write_off_product.save()
        return super(ProductListForOrder, self).save()

    def delete(self, using=None, keep_parents=False):
        if self.orderlist.paid:
            super(ProductListForOrder, self).delete()
        return_product = (ProductQuantity.objects.get(shop_id=self.store, product=self.product))
        return_product.number = return_product.number + self.count
        return_product.save()
        return super(ProductListForOrder, self).delete()

    class Meta:
        app_label = 'app_shop'
        db_table = "app_shop_productlistfororder"
