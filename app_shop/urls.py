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

authentication = [
    url(r'^$', views.authentication, name='authentication'),
    url(r'^logout$', views.logout_from_profile, name='logout_from_profile'),
    url(r'^registration$', views.registration, name='registration'),
    url(r'^user_account$', views.user_account, name='user_account'),
]

shopping = [
    url(r'^(?P<id>\w+)$', views.ProductDetailView.as_view(), name='product_detail'),
    url(r'^category/(?P<category_id>\S+)$', views.CategoryListView.as_view(), name='section_products'),
    url(r'^buy/(?P<product_id>\w+)$', views.add_product_to_cart, name='buy_product'),
    url(r'^remove_from_cart/(?P<product_id>\w+)$', views.remove_product_from_cart, name='remove_product'),
    url(r'^remove_one_copy/(?P<product_id>\w+)$', views.remove_one_copy, name='remove_one_copy'),
]

app_name = 'app_shop'
urlpatterns = [
    url(r'^$', views.main_sub_pages, name='index'),
    url(r'^cart$', views.cart, name='cart'),
    url(r'^search$', views.search, name='search'),
    url(r'^cart/send_order$', views.send_order, name='send_order'),
    url(r'^subscription$', views.subscription, name='subscription'),
    url(r'^auth/', include(authentication)),
    url(r'^shopping/', include(shopping)),
    url(r'^ru/', include(allhere_in_russia_patterns)),
    url(r'^(?P<page>\w+)?$', views.main_sub_pages, name='main_sub_pages'),
]
