from app_shop import constants
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import generic

from .forms import OrderForm, SearchForm, SubscriptionForm
from .models import News, OrderList, Promotions, Product, ProductClassification, Shops, \
    SubPagesArticle, SubscriptionEmails


def main_sub_pages(request, **kwargs):
    if kwargs:
        template_name = 'main_subpages/%s.html' % kwargs['page']
        promotions_ordinary = list(Promotions.objects.filter(for_category=None, for_carousel=False).order_by('?')[:5])
        return render(
            request,
            template_name,
            context={
                'promotions_ordinary': promotions_ordinary,
            }
        )
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
        context = {
            'news_list': News.objects.all(),
            **kwargs,
        }
        return super().get_context_data(**context)


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product_detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        if self.request.session.get('cart', None):
            cart_products = self.request.session["cart"]
            cart_products_list_id = [int(x) for x in cart_products.keys()]
        else:
            cart_products_list_id = None
        context = {
            'similiar_products': Product.objects.filter(
                classification=self.object.classification).exclude(id=self.object.id).order_by('?')[:5],
            'promotions_for_detail_page': Promotions.objects.filter(
                Q(for_category=self.object.classification_id) |
                Q(for_category=None, for_carousel=False)).order_by('?')[:5],
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
        id_list = set()

        def recursive_get(item):
            if item.category_id:
                parent = ProductClassification.objects.get(id=item.category_id)
                id_list.add(parent.id)
                recursive_get(item.category)
            else:
                return id_list

        id_list.add(self.kwargs['category_id'])
        recursive_get(category)
        if self.request.session.get('cart', None):
            cart_products = self.request.session["cart"]
            cart_products_list_id = [int(x) for x in cart_products.keys()]
        else:
            cart_products_list_id = None
        context = {
            'category': category,
            'cart_products_list_id': cart_products_list_id,
            'promotions_for_category_page': Promotions.objects.filter(
                Q(for_category__in=[obj for obj in id_list]) |
                Q(for_category=None, for_carousel=False)).order_by('?')[:5],
            **kwargs,
        }
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
        context={
            'object_list': object_list,
            'key': key,
            }
    )


def subscription(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return redirect(request.GET['next'])
    user_mail = form.cleaned_data.get("user_mail")
    SubscriptionEmails.objects.get_or_create(email=user_mail)
    return redirect(request.GET['next'])


def add_product_to_cart(request, product_id):
    if not request.session.get('cart', None):
        request.session["cart"] = {product_id: 1}
        return HttpResponseRedirect(request.GET['next'])
    else:
        if product_id in request.session['cart'].keys():
            request.session['cart'][product_id] += 1
        else:
            request.session['cart'].update({product_id: 1})
        return HttpResponseRedirect(request.GET['next'])


def del_product_from_cart(request, product_id):
    product = request.session["cart"]
    del product[product_id]
    request.session['cart'] = product
    return HttpResponseRedirect(request.GET['next'])


def del_one_copy(request, product_id):
    request.session['cart'][product_id] -= 1
    return HttpResponseRedirect(request.GET['next'])


def cart(request):
    if not request.session.get('cart', False):
        warning_min_amount = True
        list_amounts = [0, int(constants.MINIMUM_ORDER_AMOUNT)]
        return render(
            request,
            'cart.html',
            context={
                'warning_min_amount': warning_min_amount,
                'list_amounts': list_amounts,
            }
        )
    id_list = request.session["cart"]
    products_in_cart = Product.objects.filter(id__in=[int(obj) for obj in id_list.keys()])

    cost_list = {}
    for item in products_in_cart:
        cost_list[str(item.id)] = (item.price * id_list[str(item.id)])

    if sum(cost_list.values()) >= constants.MINIMUM_ORDER_AMOUNT:
        warning_min_amount = False
    else:
        warning_min_amount = True

    list_amounts = [(sum(cost_list.values())), int(constants.MINIMUM_ORDER_AMOUNT - sum(cost_list.values()))]
    order_form = OrderForm()
    return render(
        request,
        'cart.html',
        context={
            'id_list': id_list,
            'products_in_cart': products_in_cart,
            'cost_list': cost_list,
            'warning_min_amount': warning_min_amount,
            'list_amounts': list_amounts,
            'order_form': order_form,
        }
    )


def send_order(request):
    form = OrderForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect(request)
    form_data = {}
    for key, value in form.cleaned_data.items():
        if value and value != '+7':
            form_data[key] = value
    cost = int(request.GET['cost'])
    id_list = list(request.session["cart"].keys())
    obj = OrderList.objects.create(cost=cost, address=form_data['address'])
    if 'customer' in form_data.keys():
        obj.customer = form_data['customer']
    if 'customer_phone' in form_data.keys():
        obj.customer_phone = form_data['customer_phone']
    for x in id_list:
        obj.product_list.add(x)
    obj.save()
    if OrderList.objects.get(id=obj.id):
        del request.session["cart"]
    return redirect('/allhere.ru/cart')
