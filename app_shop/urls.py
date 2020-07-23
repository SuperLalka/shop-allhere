from django.conf.urls import url

from . import views


app_name = 'app_shop'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^pokupki/(?P<section>\w+)/(?P<subsection>\w+)?/(?P<paragraph>\w+)?$', views.ArticleView.as_view(), name='article_page'),
]
