# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from app_shop import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        objects = models.Product.objects.all()
        for item in objects:
            item.the_final_price = item.get_current_prices()
            print('{} is checked' .format(item.name))
            item.save()

        print('Total checked {} objects'.format(len(objects)))

