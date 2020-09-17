from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from app_shop.forms import SearchForm, SubscriptionForm
from app_shop.models import Product, ProductClassification, SubscriptionEmails


def search(request):
    form = SearchForm(request.GET)
    if not form.is_valid():
        return HttpResponseRedirect(request.path)

    key = form.cleaned_data.get("search_key")
    object_list = Product.objects.filter(Q(name__icontains=key) | Q(description__icontains=key))
    category_ids = object_list.values_list('classification_id', flat=True)
    category_list = ProductClassification.objects.filter(id__in=category_ids)
    return render(
        request,
        'search_results.html',
        context={
            'object_list': object_list,
            'key': key,
            'category_list': category_list
            }
    )


def subscription(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return redirect(request.GET['next'])

    SubscriptionEmails.objects.get_or_create(**form.cleaned_data)
    return redirect(request.GET['next'])
