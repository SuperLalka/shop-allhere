from django.conf.urls import url
from django.urls import include

from . import views


authentication = [
    url(r'^login$', views.authentication, name='authentication'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^registration$', views.registration, name='registration'),
    url(r'^user_account$', views.user_account, name='user_account'),
]

shopping = [
    url(r'^product/(?P<slug>\S+)$', views.ProductDetailView.as_view(), name='product_detail'),
    url(r'^category/(?P<category_id>\S+)$', views.CategoryListView.as_view(), name='section_products'),
    url(r'^change_user_shop/(?P<shop_id>\w+)$', views.change_user_shop, name='change_user_shop'),
    url(r'^search$', views.search, name='search'),
]

cart = [
    url(r'^$', views.cart, name='cart'),
    url(r'^add_product/(?P<product_id>\w+)$', views.add_product_to_cart, name='add_product'),
    url(r'^remove_from_cart/(?P<product_id>\w+)$', views.remove_product_from_cart, name='remove_product'),
    url(r'^remove_one_from_cart/(?P<product_id>\w+)$', views.remove_one_from_cart, name='remove_one_copy'),
    url(r'^empty_trash/', views.empty_trash, name='empty_trash'),
    url(r'^send_order$', views.send_order, name='send_order'),
]

app_name = 'app_shop'
urlpatterns = [
    url(r'^subscription$', views.subscription, name='subscription'),
    url(r'^auth/', include(authentication)),
    url(r'^cart/', include(cart)),
    url(r'^shopping/', include(shopping)),
    url(r'^(?P<page>\w+)?$', views.main_sub_pages, name='main_sub_pages'),
]
