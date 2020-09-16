# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from app_shop.models import Product, ProductQuantity
from allhere_in_russia.models import Shops


QUANTITY_OF_PRODUCT = 10


class Command(BaseCommand):

    def handle(self, *args, **options):
        products = Product.objects.all()
        shops = Shops.objects.all()
        for product in products:
            for shop in shops:
                ProductQuantity.objects.get_or_create(
                    product_id=product.id,
                    shop_id=shop.id,
                    number=QUANTITY_OF_PRODUCT
                )

                print(product.name, shop.name)
