# -*- coding: utf-8 -*-
import csv
from django.core.management.base import BaseCommand

from app_shop import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        objects = models.Shops.objects.all()
        with open('./map_objects.csv', 'w+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for item in objects:
                writer.writerow([item.longitude, item.latitude, item.address, item.name])
