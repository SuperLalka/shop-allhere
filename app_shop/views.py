from django.shortcuts import render
from django.views import generic

from .models import News, Product, Shops, SubPagesArticle


def main_sub_pages(request, **kwargs):
    template_name = 'index.html'
    if kwargs:
        template_name = 'main_subpages/%s.html' % kwargs['page']
    return render(
        request,
        template_name
    )


class SubpageAboutCompanyView(generic.DetailView):
    model = SubPagesArticle
    slug_field = 'address'
    slug_url_kwarg = 'address'

    def get_template_names(self):
        if self.object.uniq_template:
            return 'subpage_allhere_in_russia/uniq/%s.html' % self.object.address
        return 'subpage_allhere_in_russia/%s.html' % self.object.section


class ShopDetailView(generic.DetailView):
    model = Shops
    template_name = 'subpage_allhere_in_russia/uniq/shop_detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'


class NewsDetailView(generic.DetailView):
    model = News
    template_name = 'subpage_allhere_in_russia/allhere_news.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except AttributeError:
            self.object = News.objects.all().first()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'news_list': News.objects.all(),
        })
        return super().get_context_data(**context)


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'index.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 100
    template_name = 'index.html'
