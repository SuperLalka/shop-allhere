# -*- coding: utf-8 -*-
import csv
from io import open

from app_shop import models


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


def get_map_objects():
    objects = models.Shops.objects.all()
    with open('./map_objects.csv', 'w+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for item in objects:
            writer.writerow([item.longitude, item.latitude, item.address, item.name])
