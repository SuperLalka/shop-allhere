# -*- coding: utf-8 -*-
from .auth import authentication, logout, registration, user_account
from .site_function import search, filtration, subscription
from .site_rendering import main_sub_pages, ProductDetailView, CategoryListView
from .trading import add_product_to_cart, cart, change_user_shop, empty_trash, remove_product_from_cart, \
    remove_one_from_cart, send_order
