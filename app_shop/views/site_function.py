from django.db.models import Q, Min, Max
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from app_shop.forms import PriceForm, SearchForm, SubscriptionForm
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
    price_form = PriceForm(request.GET)
    if not price_form.is_valid():
        return HttpResponseRedirect(request)

    price = price_form.cleaned_data.get("price")

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

        object_list = Product.objects.filter(classification_id__in=id_list, price__lte=price)
    else:
        object_list = Product.objects.filter(classification_id=category_id, price__lte=price)

    category_list_id = object_list.values_list('classification_id', flat=True)
    category_list = ProductClassification.objects.filter(id__in=category_list_id)

    price_form = PriceForm()
    price_values = object_list.aggregate(Min('price'), Max('price'))

    return render(
        request,
        'filter_results.html',
        context={
            'object_list': object_list,
            'category': category,
            'category_list': category_list,
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
