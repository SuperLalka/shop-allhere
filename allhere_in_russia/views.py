from contextlib import suppress

from django.views import generic

from .models import News, Shops, SubPagesArticle


class SubpageAboutCompanyView(generic.DetailView):
    model = SubPagesArticle
    slug_field = 'address'
    slug_url_kwarg = 'address'

    def get_template_names(self):
        if self.object.uniq_template:
            return 'uniq/%s.html' % self.object.address
        return '%s.html' % self.object.section


class ShopDetailView(generic.DetailView):
    model = Shops
    template_name = 'uniq/shop_detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'


class NewsDetailView(generic.DetailView):
    model = News
    template_name = 'allhere_news.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_object(self, queryset=None):
        with suppress(AttributeError):
            return super().get_object()
        return News.objects.all().first()

    def get_context_data(self, **kwargs):
        return {
            'news_list': News.objects.all(),
            **super().get_context_data()
        }
