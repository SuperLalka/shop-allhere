from django.db.models import OuterRef, Subquery
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from app_shop import constants
from app_shop.forms import OrderForm
from app_shop.models import OrderList, Product, ProductListForOrder, ProductQuantity


def change_user_shop(request, shop_id):
    request.session['shop'] = int(shop_id)
    return HttpResponseRedirect(request.GET['next'])


def cart(request):
    if not request.session.get('cart', False):
        return render(request, 'cart.html', context={
                'total_cost': 0,
                'shortage': constants.MINIMUM_ORDER_AMOUNT}
        )

    products_quantity = ProductQuantity.objects.filter(
        shop_id=request.session['shop'],
        product_id=OuterRef('id')
    )

    products_ids = request.session["cart"]
    products_in_cart = Product.objects.filter(id__in={**products_ids}.keys()).annotate(
        count=Subquery(products_quantity.values_list('number', flat=True)[:1]))

    cost_list = {
        str(item.id): round(float(item.get_current_prices()) * products_ids[str(item.id)], 2)
        for item in products_in_cart
    }

    total_cost = round(sum(cost_list.values()), 2)
    shortage = round(constants.MINIMUM_ORDER_AMOUNT - sum(cost_list.values()), 2)

    return render(
        request,
        'cart.html',
        context={
            'order_form': OrderForm(),
            'products_in_cart': products_in_cart,
            'cost_list': cost_list,
            'total_cost': total_cost,
            'shortage': shortage,
        }
    )


def add_product_to_cart(request, product_id):
    count = request.session['cart'].get(product_id, 0)
    request.session['cart'][int(product_id)] = count + 1
    return HttpResponseRedirect(request.GET['next'])


def remove_product_from_cart(request, product_id):
    if product_id in request.session['cart']:
        request.session["cart"].pop(product_id)
    return HttpResponseRedirect(request.GET['next'])


def remove_one_from_cart(request, product_id):
    if product_id in request.session['cart']:
        count = request.session['cart'].get(product_id, 0)

        if count <= 1:
            request.session["cart"].pop(product_id)
            return HttpResponseRedirect(request.GET['next'])

        request.session['cart'][product_id] -= 1
    return HttpResponseRedirect(request.GET['next'])


def empty_trash(request):
    request.session['cart'] = {}
    return redirect('/allhere.ru/cart/')


def send_order(request):
    form = OrderForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect(request.path)

    products_id = request.session["cart"]
    products_in_cart = Product.objects.filter(id__in={**products_id}.keys())

    cost_list = {
        str(item.id): float(item.get_current_prices()) * products_id[str(item.id)]
        for item in products_in_cart
    }
    total_cost = round(sum(cost_list.values()), 2)

    form_data = {
        key: value
        for key, value in form.cleaned_data.items() if value
    }

    if request.user.is_authenticated:
        form_data['customer_id'] = request.user.id

    obj = OrderList.objects.create(
        cost=total_cost,
        **form_data
    )

    for name, count in request.session["cart"].items():
        ProductListForOrder.objects.create(
            orderlist_id=obj.id,
            product_id=name,
            store=request.session['shop'],
            count=count
        )

    request.session["cart"] = {}
    return redirect('/allhere.ru/cart/')
