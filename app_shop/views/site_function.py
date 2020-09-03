from django.db.models import Q, Min, Max
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from app_shop.forms import BrandsForm, PriceForm, SearchForm, SubscriptionForm
from app_shop.models import Product, ProductClassification, SubscriptionEmails


def search(request):
    form = SearchForm(request.GET)
    if not form.is_valid():
        return HttpResponseRedirect(request)

    key = form.cleaned_data.get("search_key")
    object_list = Product.objects.filter(Q(name__icontains=key) | Q(description__icontains=key))
    category_list_id = object_list.values_list('classification_id', flat=True)
    category_list = ProductClassification.objects.filter(id__in=category_list_id)
    return render(
        request,
        'search_results.html',
        context={
            'object_list': object_list,
            'key': key,
            'category_list': category_list
            }
    )


def filtration(request, category_id):
    query_dictionary = {}

    price_form = PriceForm(request.GET)
    if not price_form.is_valid():
        return HttpResponseRedirect(request)

    if price_form.cleaned_data.get("price"):
        query_dictionary['price__lte'] = price_form.cleaned_data.get("price")

    if request.GET.getlist('brand'):
        query_dictionary['specifications__Бренд__in'] = request.GET.getlist('brand')

    category = ProductClassification.objects.get(id=category_id)
    subcategories_qs = ProductClassification.objects.filter(category_id=category_id)
    if subcategories_qs:

        def get_childs(item):
            childs = ProductClassification.objects.filter(category_id=item.id)
            for child in childs:
                id_list.add(child.id)

        id_list = set()
        for obj in subcategories_qs:
            id_list.add(obj.id)
            get_childs(obj)

        query_dictionary['classification_id__in'] = id_list
    else:
        query_dictionary['classification_id'] = category_id

    object_list = Product.objects.filter(**query_dictionary)
    category_list_id = object_list.values_list('classification_id', flat=True)
    category_list = ProductClassification.objects.filter(id__in=category_list_id)

    specifications = object_list.values_list('specifications', flat=True)
    brands_names = set([x['Бренд'] if 'Бренд' in x.keys() else 'Не указано' for x in specifications])
    brands_form = BrandsForm(choices=brands_names)

    price_values = object_list.aggregate(Min('price'), Max('price'))
    price_form = PriceForm()

    return render(
        request,
        'filter_results.html',
        context={
            'object_list': object_list,
            'category': category,
            'category_list': category_list,
            'brands_form': brands_form,
            'brands_names': brands_names,
            'price_form': price_form,
            'price_values': price_values,
        }
    )


def subscription(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return redirect(request.GET['next'])

    user_mail = form.cleaned_data.get("user_mail")
    SubscriptionEmails.objects.get_or_create(email=user_mail)
    return redirect(request.GET['next'])
