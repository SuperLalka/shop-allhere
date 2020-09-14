from django.db.models.signals import post_save, pre_delete
from django.dispatch.dispatcher import receiver

from .models import Product, ProductClassification, Promotions, PromotionsForCategory


@receiver(pre_delete, sender=Product)
def image_model_delete(instance, **kwargs):
    if instance.images.name != "1_DEFAULT_IMAGE.jpg":
        instance.images.delete(False)


@receiver(pre_delete, sender=Promotions)
def image_model_delete(instance, **kwargs):
    if instance.images.name:
        instance.images.delete(False)


@receiver(post_save, sender=PromotionsForCategory)
def cascading_category_assignment(instance, **kwargs):
    category = ProductClassification.objects.get(id=instance.category_id)

    def recursive_get(x):
        yield x.id
        for child in ProductClassification.objects.filter(category_id=x.id):
            yield from recursive_get(child)

    category_id_list = list(recursive_get(category))

    qs = Product.objects.filter(classification_id__in=category_id_list)
    for item in qs:
        item.the_final_price = item.get_current_prices()
        item.save()
