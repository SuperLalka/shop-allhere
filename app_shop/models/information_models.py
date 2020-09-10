from django.db import models


class SubscriptionEmails(models.Model):
    email = models.EmailField(max_length=40, help_text="Enter email for mailing", unique=True)

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'app_shop'
        verbose_name = 'Mailing address'
        verbose_name_plural = 'Postal addresses'
