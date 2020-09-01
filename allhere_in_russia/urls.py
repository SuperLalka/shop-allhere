from django.conf.urls import url
from django.views.generic import RedirectView

from . import views


app_name = 'allhere_in_russia'
urlpatterns = [
    url(r'^$', RedirectView.as_view(url='allhere_in_russia', permanent=False), name='subpage_index'),
    url(r'^(?P<address>\w+)$', views.SubpageAboutCompanyView.as_view(), name='subpages'),
    url(r'^all_shops/(?P<id>\w+)$', views.ShopDetailView.as_view(), name='shop_detail'),
    url(r'^news/(?P<id>\w+)?$', views.NewsDetailView.as_view(), name='news'),
]
