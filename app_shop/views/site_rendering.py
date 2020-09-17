import random
from django.db.models import Count, Max, Min, Subquery, OuterRef
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from app_shop.forms import PriceForm, FiltersForm
from app_shop.models import ClassificationFilters, FiltersForClassifications, Promotions, Product, \
    ProductClassification, ProductListForOrder, ProductQuantity
from shop_allhere.utils import get_promotions_for_category


def main_sub_pages(request, **kwargs):
    context_content = {}
    if not kwargs:
        template_name = 'index.html'
        context_content['promotions_for_carousel'] = Promotions.objects.filter(for_carousel=True)
        context_content['highest_categories'] = ProductClassification.objects.filter(highest_category=True)
    else:
        template_name = 'main_subpages/%s.html' % kwargs['page']

    context_content['promotions_ordinary'] = list(Promotions.objects.filter(
        for_category=None, for_carousel=False).order_by('?')[:5])
    return render(request, template_name, context={**context_content})


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        self.object.count = (ProductQuantity.objects.get(
            shop_id=self.request.session['shop'], product_id=self.object.id)).number

        list_orders_id = ProductListForOrder.objects.filter(
            product_id=self.object.id).values_list('orderlist_id', flat=True)
        most_often_buy = ProductListForOrder.objects.filter(
            orderlist_id__in=list_orders_id).exclude(product_id=self.object.id).values('product_id').annotate(
            count=Count("id")).order_by('-count')[:5]
        most_often_buy = most_often_buy.values_list('product_id', flat=True)
        also_buy_products = Product.objects.filter(id__in=most_often_buy)

        similiar_products = Product.objects.filter(
            classification=self.object.classification).exclude(
            id=self.object.id).order_by('?')[:5]

        promotions_for_page = get_promotions_for_category([self.object.classification_id])

        context = {
            'also_buy_products': also_buy_products,
            'similiar_products': similiar_products,
            'promotions_for_page': promotions_for_page,
            **kwargs
        }
        return super().get_context_data(**context)


class CategoryListView(generic.ListView):
    model = ProductClassification
    template_name = 'section_products.html'

    def get_queryset(self):
        query_dictionary = {}
        order = self.request.GET.get('sorted', None)
        if order not in ['price', '-price']:
            order = 'name'

        if self.kwargs:
            filters_form = FiltersForm(self.request.GET)
            if not filters_form.is_valid():
                return HttpResponseRedirect(self.request.path)

            for filter_key, filter_value in filters_form.data.items():
                if filter_key != 'price' and filter_value:
                    filter_obj = FiltersForClassifications.objects.filter(name=filter_key).first()
                    if filter_obj:
                        if filter_obj.type == "INT":
                            query_dictionary['specifications__' + filter_key + '__lte'] = float(filter_value)
                        elif filter_obj.type == "CSM":
                            query_dictionary['specifications__' + filter_key + '__in'] = self.request.GET.getlist(filter_key)
                elif filter_value:
                    query_dictionary['the_final_price__lte'] = float(filter_value)

        def recursive_get_childs(item):
            yield item.id
            for child in item.get_child():
                yield from recursive_get_childs(child)

        self.kwargs['category'] = ProductClassification.objects.get(id=self.kwargs['category_id'])
        self.kwargs['category_ids'] = list(recursive_get_childs(self.kwargs['category']))
        query_dictionary['classification_id__in'] = self.kwargs['category_ids']

        products_quantity = ProductQuantity.objects.filter(
            shop_id=self.request.session['shop'],
            product_id=OuterRef('id')
        )
        self.queryset = Product.objects.filter(**query_dictionary).order_by(order).annotate(
            count=Subquery(products_quantity.values_list('number', flat=True)[:1])
        )
        return self.queryset

    def get_context_data(self, **kwargs):
        form_dictionary = {}

        self.kwargs['category_ids'] = self.queryset.values_list('classification_id', flat=True)
        category_list = ProductClassification.objects.filter(id__in=self.kwargs['category_ids'])

        promotions_for_page = get_promotions_for_category(self.kwargs['category_ids'])
        product_listing_ads = Promotions.objects.filter(obligatory=True).order_by("?").first()
        product_listing_ads.serial_number = random.randint(5, 10)

        price_values = self.queryset.aggregate(
            min_price=Min('the_final_price'), max_price=Max('the_final_price'))
        price_form = PriceForm(min_value=price_values['min_price'])
        form_dictionary['price_form'] = price_form

        filter_list = ClassificationFilters.objects.filter(
            classification_id=self.kwargs['category_id']).values('filter__name', 'filter__type', 'filter__priority')

        form_filters = []
        for filter_object in filter_list:
            if filter_object['filter__type'] != 'TXT':
                value = self.queryset.values_list('specifications__' + filter_object['filter__name'], flat=True)
                if filter_object['filter__type'] == 'INT':
                    filter_object['filter__values'] = [min(value), max(value)]
                elif filter_object['filter__type'] == 'CSM':
                    filter_object['filter__values'] = value
            form_filters.append(filter_object)

        filters_form = FiltersForm(filters=form_filters)
        form_dictionary['filters_form'] = filters_form

        context = {
            'category': self.kwargs['category'],
            'category_list': category_list,
            'promotions_for_page': promotions_for_page,
            'product_listing_ads': product_listing_ads,
            'price_values': price_values,
            **form_dictionary,
            **kwargs,
        }
        return super().get_context_data(**context)
