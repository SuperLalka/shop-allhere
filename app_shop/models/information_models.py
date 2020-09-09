from django.db import models
from tinymce.models import HTMLField

from app_shop.models import ProductClassification


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
    for_category = models.ManyToManyField('ProductClassification', through='PromotionsForCategory')

    def __str__(self):
        return '{0} ({1} - {2})'.format(self.name, self.start_time, self.end_time)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Promotions, self).save()
        category_list = PromotionsForCategory.objects.filter(promotion_id=self.id)
        for item in category_list:
            subcategories_qs = ProductClassification.objects.filter(category_id=item.category.id)
            if subcategories_qs:

                def recursive_get(item):
                    if item.category:
                        child_list = ProductClassification.objects.filter(category_id=item.id)
                        for child in child_list:
                            id_list.add(child.id)
                            recursive_get(item.category)
                    else:
                        return id_list

                for obj in subcategories_qs:
                    id_list = {obj.id}
                    recursive_get(obj)

                    for num in id_list:
                        PromotionsForCategory.objects.get_or_create(promotion_id=self.id,
                                                                    category_id=num,
                                                                    discount=item.discount)

        return super(Promotions, self).save()

    def list_categories(self):
        return self.objects.for_category

    class Meta:
        app_label = 'app_shop'
        ordering = ('-end_time',)
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'


class PromotionsForCategory(models.Model):
    promotion = models.ForeignKey('Promotions', on_delete=models.CASCADE)
    category = models.ForeignKey('ProductClassification', on_delete=models.CASCADE)
    discount = models.PositiveSmallIntegerField()

    class Meta:
        app_label = 'app_shop'
        db_table = "app_shop_promotionsforcategory"


class SubscriptionEmails(models.Model):
    email = models.EmailField(max_length=40, help_text="Enter email for mailing", unique=True)

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'app_shop'
        verbose_name = 'Mailing address'
        verbose_name_plural = 'Postal addresses'
