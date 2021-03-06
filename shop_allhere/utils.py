# -*- coding: utf-8 -*-
import json
from django.contrib.postgres.forms.jsonb import InvalidJSONInput, JSONField
from django.db.models import Q


def transliterate(name):
    """Транслитерация значения name"""
    slovar = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
        'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
        'ю': 'u', 'я': 'ja', 'А': 'a', 'Б': 'b', 'В': 'v', 'Г': 'g', 'Д': 'd', 'Е': 'e', 'Ё': 'e',
        'Ж': 'zh', 'З': 'z', 'И': 'i', 'Й': 'i', 'К': 'k', 'Л': 'l', 'М': 'm', 'Н': 'n',
        'О': 'o', 'П': 'p', 'Р': 'r', 'С': 's', 'Т': 't', 'У': 'u', 'Ф': 'f', 'Х': 'h',
        'Ц': 'c', 'Ч': 'cz', 'Ш': 'sh', 'Щ': 'scz', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'e',
        'Ю': 'u', 'Я': 'ja', ',': '', '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '',
        '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
        ':': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '', '№': '',
        '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
        'Є': 'e'
    }
    for key in slovar:
        name = name.replace(key, slovar[key])
    return name.lower()


class ReadableJSONFormField(JSONField):
    def prepare_value(self, value):
        if isinstance(value, InvalidJSONInput):
            return value
        return json.dumps(value, ensure_ascii=False, indent=2)


def get_promotions_for_category(list_categories):
    from app_shop.models import Promotions

    quantity_promotions = Promotions.objects.filter(advertising__obligatory=True)[:5]
    occupied_indexes = quantity_promotions.values_list('advertising__idx_among_promotions', flat=True)

    all_indexes = list(range(5))
    required_indexes = list(set(all_indexes) - set(occupied_indexes))
    if len(required_indexes) > 0:
        promotions = Promotions.objects.filter(
                    Q(for_category__in=list_categories) |
                    Q(for_category=None, for_carousel=False, advertising=None)).order_by('?')[:len(required_indexes)]

        quantity_promotions = quantity_promotions.union(promotions)

    quantity_promotions = list(quantity_promotions.order_by('-advertising'))
    idx_to_item = []
    for index, promo in enumerate(quantity_promotions):
        idx_to_item.append([
            promo.advertising.idx_among_promotions if promo.advertising else required_indexes[index],
            promo,
        ])

    quantity_promotions = map(lambda x: x[1], sorted(idx_to_item, key=lambda x: x[0]))
    return quantity_promotions
