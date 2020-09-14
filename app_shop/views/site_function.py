from django.db.models import Q, Min, Max
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from app_shop.forms import PriceForm, SearchForm, SubscriptionForm, VariableFiltersForm
from app_shop.models import ClassificationFilters, FiltersForClassifications, Product, ProductClassification, \
    Promotions, SubscriptionEmails


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
    form_dictionary = {}
    form_filters = []
    query_dictionary = {}

    variable_filters_form = VariableFiltersForm(request.GET)
    if not variable_filters_form.is_valid():
        return HttpResponseRedirect(request)

    for item, value in variable_filters_form.data.items():
        if item != 'price' and value:
            item_type = (FiltersForClassifications.objects.get(name=item)).type
            if item_type == "INT":
                if value.isdigit():
                    query_dictionary['specifications__' + item + '__lte'] = int(value)
                else:
                    query_dictionary['specifications__' + item + '__lte'] = float(value)
            elif item_type == "CSM":
                query_dictionary['specifications__' + item + '__in'] = request.GET.getlist(item)
        else:
            if value:
                query_dictionary['price__lte'] = float(value)

    category = ProductClassification.objects.get(id=category_id)

    def get_childs(item):
        yield item.id
        for child in item.get_child():
            yield from get_childs(child)

    category_id_list = list(get_childs(category))
    query_dictionary['classification_id__in'] = category_id_list

    promotions_for_category_page = Promotions.objects.filter(
        Q(for_category__in=category_id_list) |
        Q(for_category=None, for_carousel=False)).order_by('?')[:5]

    object_list = Product.objects.filter(**query_dictionary)
    category_list_id = object_list.values_list('classification_id', flat=True)
    category_list = ProductClassification.objects.filter(id__in=category_list_id)

    objects_in_category = Product.objects.filter(classification_id__in=category_id_list)
    price_values = objects_in_category.aggregate(
        min_price=Min('the_final_price'), max_price=Max('the_final_price'))
    price_form = PriceForm(request.GET, min_value=price_values['min_price'])
    form_dictionary['price_form'] = price_form

    filter_list = ClassificationFilters.objects.filter(
        classification_id=category.id).values('filter__name', 'filter__type', 'filter__priority')

    for obj in filter_list:
        if obj['filter__type'] != 'TXT':
            value = objects_in_category.values_list('specifications__' + obj['filter__name'], flat=True)
            value = [value for value in value if value]
            if obj['filter__type'] == 'INT':
                obj['filter__values'] = [min(value), max(value)]
            elif obj['filter__type'] == 'CSM':
                obj['filter__values'] = value
        form_filters.append(obj)

    variable_filters_form = VariableFiltersForm(request.GET, filters=form_filters)
    form_dictionary['variable_filters_form'] = variable_filters_form

    return render(
        request,
        'section_products.html',
        context={
            'object_list': object_list,
            'category': category,
            'category_list': category_list,
            'promotions_for_category_page': promotions_for_category_page,
            'price_values': price_values,
            **form_dictionary
        }
    )


def subscription(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return redirect(request.GET['next'])

    SubscriptionEmails.objects.get_or_create(**form.cleaned_data)
    return redirect(request.GET['next'])
