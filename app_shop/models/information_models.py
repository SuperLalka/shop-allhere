from django.db import models
from tinymce.models import HTMLField


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
        app_label = 'app_shop'
        ordering = ('-end_time',)
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'


class SubscriptionEmails(models.Model):
    email = models.EmailField(max_length=40, help_text="Enter email for mailing", unique=True)

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'app_shop'
        verbose_name = 'Mailing address'
        verbose_name_plural = 'Postal addresses'
