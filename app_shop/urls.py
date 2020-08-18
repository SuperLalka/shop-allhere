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

app_name = 'app_shop'
urlpatterns = [
    url(r'^$', views.main_sub_pages, name='index'),
    url(r'^(?P<page>\w+)?$', views.main_sub_pages, name='main_sub_pages'),
    url(r'^shopping/(?P<id>\w+)$', views.ProductDetailView.as_view(), name='product_detail'),
    url(r'^shopping/category/(?P<category_id>\S+)$', views.CategoryListView.as_view(), name='section_products'),
    url(r'^ru/', include(allhere_in_russia_patterns)),
]
