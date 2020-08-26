from django.conf.urls import url
from django.views.generic import RedirectView
from django.urls import include

from . import views


allhere_in_russia_patterns = [
    url(r'^$', RedirectView.as_view(url='allhere_in_russia', permanent=False), name='subpage_index'),
    url(r'^(?P<address>\w+)$', views.SubpageAboutCompanyView.as_view(), name='subpage_allhere_in_russia'),
    url(r'^all_shops/(?P<id>\w+)$', views.ShopDetailView.as_view(), name='shop_detail'),
    url(r'^news/(?P<id>\w+)?$', views.NewsDetailView.as_view(), name='news'),
]

shopping = [
    url(r'^(?P<id>\w+)$', views.ProductDetailView.as_view(), name='product_detail'),
    url(r'^buy/(?P<product_id>\w+)$', views.add_product_to_cart, name='buy_product'),
    url(r'^del_from_cart/(?P<product_id>\w+)$', views.del_product_from_cart, name='delete_product'),
    url(r'^del_one_copy/(?P<product_id>\w+)$', views.del_one_copy, name='delete_one_copy'),
    url(r'^category/(?P<category_id>\S+)$', views.CategoryListView.as_view(), name='section_products'),
]

app_name = 'app_shop'
urlpatterns = [
    url(r'^$', views.main_sub_pages, name='index'),
    url(r'^cart$', views.cart, name='cart'),
    url(r'^cart/send_order$', views.send_order, name='send_order'),
    url(r'^search$', views.search, name='search'),
    url(r'^subscription$', views.subscription, name='subscription'),
    url(r'^(?P<page>\w+)?$', views.main_sub_pages, name='main_sub_pages'),
    url(r'^shopping/', include(shopping)),
    url(r'^ru/', include(allhere_in_russia_patterns)),
]
