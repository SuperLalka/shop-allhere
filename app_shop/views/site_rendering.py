from django.db.models import Q, Count, Max, Min
from django.shortcuts import render
from django.views import generic

from app_shop.models import Promotions, Product, ProductClassification, ProductListForOrder
from app_shop.forms import PriceForm


def main_sub_pages(request, **kwargs):
    if kwargs:
        template_name = 'main_subpages/%s.html' % kwargs['page']
        promotions_ordinary = list(Promotions.objects.filter(
            for_category=None, for_carousel=False).order_by('?')[:5])
        return render(request, template_name, context={'promotions_ordinary': promotions_ordinary})

    template_name = 'index.html'
    promotions_carousel = Promotions.objects.filter(for_carousel=True)
    promotions_ordinary = list(Promotions.objects.filter(for_category=None, for_carousel=False).order_by('?')[:5])
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


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product_detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        list_orders_id = ProductListForOrder.objects.filter(
            product_id=self.object.id).values_list('orderlist_id', flat=True)
        most_often_buy = ProductListForOrder.objects.filter(
            orderlist_id__in=list_orders_id).exclude(product_id=self.object.id).values('product_id').annotate(
            count=Count("id")).order_by('-count')[:5]
        most_often_buy = most_often_buy.values_list('product_id', flat=True)
        also_buy_products = ProductListForOrder.objects.filter(
            product_id__in=most_often_buy).distinct('product_id')

        if self.request.session.get('cart', None):
            cart_products = self.request.session["cart"]
            cart_products_list_id = [int(x) for x in cart_products.keys()]
        else:
            cart_products_list_id = None

        similiar_products = Product.objects.filter(
            classification=self.object.classification).exclude(
            id=self.object.id).order_by('?')[:5]
        promotions_for_detail_page = Promotions.objects.filter(
            Q(for_category=self.object.classification_id) |
            Q(for_category=None, for_carousel=False)).order_by('?')[:5]

        context = {
            'also_buy_products': also_buy_products,
            'similiar_products': similiar_products,
            'promotions_for_detail_page': promotions_for_detail_page,
            'cart_products_list_id': cart_products_list_id,
            **kwargs
        }
        return super().get_context_data(**context)


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
                recursive_get(obj)
            self.queryset = Product.objects.filter(classification_id__in=[obj for obj in id_list])
            return self.queryset
        else:
            self.queryset = Product.objects.filter(classification_id=self.kwargs['category_id'])
            return self.queryset

    def get_context_data(self, **kwargs):
        category = ProductClassification.objects.get(id=self.kwargs['category_id'])
        category_list_id = self.queryset.values_list('classification_id', flat=True)
        category_list = ProductClassification.objects.filter(id__in=category_list_id)

        def recursive_get(item):
            if item.category_id:
                parent = ProductClassification.objects.get(id=item.category_id)
                id_list.add(parent.id)
                recursive_get(item.category)

        id_list = set()
        id_list.add(self.kwargs['category_id'])
        recursive_get(category)

        if self.request.session.get('cart', None):
            cart_products = self.request.session["cart"]
            cart_products_list_id = [int(x) for x in cart_products.keys()]
        else:
            cart_products_list_id = None

        promotions_for_category_page = Promotions.objects.filter(
            Q(for_category__in=id_list) |
            Q(for_category=None, for_carousel=False)).order_by('?')[:5]

        price_values = self.queryset.aggregate(Min('price'), Max('price'))
        specifications = self.queryset.values_list('specifications', flat=True)

        price_form = PriceForm()

        context = {
            'category': category,
            'category_list': category_list,
            'cart_products_list_id': cart_products_list_id,
            'promotions_for_category_page': promotions_for_category_page,
            'price_values': price_values,
            'specifications': specifications,
            'price_form': price_form,
            **kwargs,
        }
        return super().get_context_data(**context)
