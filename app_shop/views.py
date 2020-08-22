from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from .forms import SearchForm
from .models import News, Promotions, Product, ProductClassification, Shops, SubPagesArticle


def main_sub_pages(request, **kwargs):
    if kwargs:
        template_name = 'main_subpages/%s.html' % kwargs['page']
        return render(
            request,
            template_name
        )
    template_name = 'index.html'
    promotions_carousel = Promotions.objects.filter(for_carousel=True)
    promotions_ordinary = list(Promotions.objects.filter(for_carousel=False).order_by('?')[:5])

    highest_categories = ProductClassification.objects.filter(highest_category=True)
    return render(
        request,
        template_name,
        context={
            'promotions_for_carousel': promotions_carousel,
            'promotions_ordinary': promotions_ordinary,
            'highest_categories': highest_categories,
        }
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
    template_name = 'product_detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'


class CategoryListView(generic.ListView):
    model = Product
    template_name = 'section_products.html'
    slug_field = 'classification_id'
    slug_url_kwarg = 'classification_id'

    def get_queryset(self):
        subcategories_qs = ProductClassification.objects.filter(category_id=self.kwargs['category_id'])
        if subcategories_qs:
            id_list = set()

            def recursive_get(item):
                if item.category:
                    child_list = ProductClassification.objects.filter(category_id=item.id)
                    for child in child_list:
                        id_list.add(child.id)
                        recursive_get(item.category)
                else:
                    return id_list

            for obj in subcategories_qs:
                id_list.add(obj.id)
                item = recursive_get(obj)
            self.queryset = Product.objects.filter(classification_id__in=[obj for obj in id_list])
            return self.queryset
        else:
            self.queryset = Product.objects.filter(classification_id=self.kwargs['category_id'])
            return self.queryset


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
        'category': ProductClassification.objects.get(id=self.kwargs['category_id']).name,
    })
    return super().get_context_data(**context)


def search(request):
    form = SearchForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect(request)
    key = form.cleaned_data.get("search_key")
    object_list = Product.objects.filter(Q(name__icontains=key) | Q(description__icontains=key))
    return render(
        request,
        'search_results.html',
        context={'object_list': object_list,
                 'key': key,
                 }
    )
