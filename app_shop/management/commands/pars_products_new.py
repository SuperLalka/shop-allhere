# -*- coding: utf-8 -*-
import requests
import os
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from app_shop import models
from shop_allhere import settings


class Command(BaseCommand):

    def handle(self, *args, **options):

        def create_product_objects(soup_obj, category):
            products_list = soup_obj.find_all(attrs={"class": "linkToPDP"})
            for product in products_list:
                product_address = product['href']
                product_resp = requests.get("https://www.auchan.ru" + product_address)
                product_soup = BeautifulSoup(product_resp.text, 'html.parser')
                product_slug = product_address.split('/')[-2]

                image = product_soup.find('div', {"class": "product-carousel"}).find('img')
                image = image.get('src') if image else 'products/1_DEFAULT_IMAGE.jpg'

                image_name = '{}.jpg'.format(product_slug)[:85]
                image_address = 'products/{}'.format(image_name)
                image_url = requests.get(host + image)

                file_address = os.path.join(settings.MEDIA_ROOT, 'products/{}'.format(image_name))
                file = open(file_address, 'wb')
                file.write(image_url.content)
                file.close()

                product_name = product_soup.find('h1', {"id": "productName"}).text
                product_price = float(product_soup.find('div', {"class": "fullPricePDP"}).next_element.replace(' ', ''))
                product_description = product_soup.find('div', {"class": "css-ivaahx"}).text

                product_specifications = product_soup.find('tbody')
                prod_spec_dict = {}
                for table_row in product_specifications.find_all('tr'):
                    prod_spec_dict[table_row.find('th').text] = table_row.find('td').text

                models.Product.objects.create(name=product_name,
                                              price=product_price,
                                              description=product_description,
                                              images=image_address,
                                              classification=category,
                                              specifications=prod_spec_dict,
                                              slug=product_slug)

        host = "https://www.auchan.ru/"
        resp = requests.get(host)
        soup = BeautifulSoup(resp.text, 'html.parser')
        category_block = soup.find_all(attrs={"class": "youMayNeedCategoryItem"})

        for obj in category_block:
            category_slug = obj['href']
            parent_category, _ = models.ProductClassification.objects.get_or_create(
                name=obj.text.upper(), highest_category=True, slug=category_slug.split('/')[-2])
            subresp = requests.get("https://www.auchan.ru" + category_slug)
            sub_soup = BeautifulSoup(subresp.text, 'html.parser')
            other_category = sub_soup.find_all(attrs={"class": "linkToSubCategory"})

            for item in other_category:
                subcategory_slug = item['href']
                sub_category, _ = models.ProductClassification.objects.get_or_create(
                    name=item.text, category_id=parent_category.id, slug=subcategory_slug.split('/')[-2])
                lowresp = requests.get("https://www.auchan.ru" + subcategory_slug)
                low_soup = BeautifulSoup(lowresp.text, 'html.parser')
                lower_category = low_soup.find(attrs={"id": "categoriesThirdLvlList"})

                if lower_category:
                    for x in lower_category.find_all('a'):
                        lower_slug = x['href']
                        low_category, _ = models.ProductClassification.objects.get_or_create(
                            name=x.text, category_id=sub_category.id, slug=lower_slug.split('/')[-2])
                        lower_resp = requests.get("https://www.auchan.ru" + lower_slug)
                        lower_soup = BeautifulSoup(lower_resp.text, 'html.parser')
                        create_product_objects(lower_soup, low_category)
                else:
                    create_product_objects(low_soup, sub_category)
