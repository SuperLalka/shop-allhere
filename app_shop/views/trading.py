from app_shop import constants
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from app_shop.forms import OrderForm
from app_shop.models import OrderList, Product, ProductListForOrder


def cart(request):
    if not request.session.get('cart', False):
        return render(request, 'cart.html', context={
                'total_cost': 0,
                'disadvantage': constants.MINIMUM_ORDER_AMOUNT}
        )
    products_id = request.session["cart"]
    products_in_cart = Product.objects.filter(id__in={**products_id}.keys())

    cost_list = {
        str(item.id): float(item.get_current_prices()) * products_id[str(item.id)]
        for item in products_in_cart
    }

    total_cost = round(sum(cost_list.values()), 2)
    disadvantage = constants.MINIMUM_ORDER_AMOUNT - sum(cost_list.values())

    return render(
        request,
        'cart.html',
        context={
            'order_form': OrderForm(),
            'products_id': products_id,
            'products_in_cart': products_in_cart,
            'cost_list': cost_list,
            'total_cost': total_cost,
            'disadvantage': disadvantage,
        }
    )


def add_product_to_cart(request, product_id):
    if not request.session.get('cart'):
        request.session["cart"] = {}

    count = request.session['cart'].get(product_id, 0)
    request.session['cart'][int(product_id)] = count + 1

    return HttpResponseRedirect(request.GET['next'])


def remove_product_from_cart(request, product_id):
    if request.session.get('cart'):
        if product_id in request.session['cart']:
            request.session["cart"].pop(product_id)
    return HttpResponseRedirect(request.GET['next'])


def remove_one_from_cart(request, product_id):
    if request.session.get('cart'):
        if product_id in request.session['cart']:
            count = request.session['cart'].get(product_id, 0)

            if count <= 1:
                request.session["cart"].pop(product_id)
                return HttpResponseRedirect(request.GET['next'])

            request.session['cart'][product_id] -= 1
    return HttpResponseRedirect(request.GET['next'])


def send_order(request):
    form = OrderForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect(request)

    form_data = {
        key: value
        for key, value in form.cleaned_data.items() if value
    }

    if request.user.is_authenticated:
        form_data['customer_id'] = request.user.id

    obj = OrderList.objects.create(
        cost=float(request.GET['total_cost']),
        **form_data
    )

    for name, count in request.session["cart"].items():
        ProductListForOrder.objects.create(
            orderlist_id=obj.id,
            product_id=name,
            count=count
        )
    del request.session["cart"]

    return redirect('/allhere.ru/cart/')
