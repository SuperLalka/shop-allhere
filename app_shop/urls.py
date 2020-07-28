from django.conf.urls import url
from django.views.generic import RedirectView
from django.urls import include

from . import views


allhere_in_russia_patterns = [
    url(r'^$', RedirectView.as_view(url='allhere_in_russia', permanent=False), name='subpage_index'),
    url(r'^(?P<address>\w+)$', views.SubpageAboutCompanyView.as_view(), name='subpage_allhere_in_russia'),
]

app_name = 'app_shop'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ru/', include(allhere_in_russia_patterns))
    #url(r'^pokupki/(?P<section>\w+)/(?P<subsection>\w+)?/(?P<paragraph>\w+)?$', views.ArticleView.as_view(), name='article_page'),
]
