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
    subcategories_qs = ProductClassification.objects.filter(category_id=instance.category_id)
    if subcategories_qs:

        def recursive_get(x):
            child_list = ProductClassification.objects.filter(category_id=x.id)
            if child_list:
                for child in child_list:
                    category_id_list.append(child.id)
                    recursive_get(x.category)
            else:
                return category_id_list

        for obj in subcategories_qs:
            category_id_list = [obj.id]
            recursive_get(obj)

            qs = Product.objects.filter(classification_id__in=category_id_list)
            for item in qs:
                item.the_final_price = item.get_current_prices()
                item.save()
