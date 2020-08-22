# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from app_shop import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        resp = requests.get("https://www.auchan.ru/")
        soup = BeautifulSoup(resp.text, 'html.parser')
        category_block = soup.find_all(attrs={"class": "m-menu__item"})
        for obj in category_block:
            top_category = obj.find(attrs={"class": "m-menu__txt"})
            parent_category, _ = models.ProductClassification.objects.get_or_create(name=top_category.text.upper(), highest_category=True)
            other_category = obj.find_all(attrs={"class": "m-menu__submenu-item-link"})
            act_category = ""
            for x in other_category:
                item = re.search(r'/pokupki/[a-z-]+?/[a-z-]+?.html\">(.+?)</a>', str(x))
                if item:
                    act_category, _ = models.ProductClassification.objects.get_or_create(name=x.text, category_id=parent_category.id)
                else:
                    lower_category = models.ProductClassification.objects.get_or_create(name=x.text, category_id=act_category.id)
        
