from django.db import models


class SubscriptionEmails(models.Model):
    email = models.EmailField(max_length=40, help_text="Enter email for mailing", unique=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Mailing address'
        verbose_name_plural = 'Postal addresses'


class VisitStatistics(models.Model):
    url_address = models.CharField(max_length=200)
    user_id = models.PositiveSmallIntegerField(null=True, blank=True)
    actions = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Page visit'
        verbose_name_plural = 'Page visits'
