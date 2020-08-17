from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from .models import Product


@receiver(pre_delete, sender=Product)
def image_model_delete(sender, instance, **kwargs):
    if instance.images.name:
        instance.images.delete(False)
