from app_shop import constants
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from app_shop.forms import OrderForm
from app_shop.models import OrderList, Product, ProductListForOrder


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
    order_form = OrderForm()
    id_list = request.session["cart"]
    products_in_cart = Product.objects.filter(id__in=[int(obj) for obj in id_list.keys()])

    cost_list = {}
    for item in products_in_cart:
        cost_list[str(item.id)] = (float(item.get_current_prices()) * id_list[str(item.id)])

    if sum(cost_list.values()) >= constants.MINIMUM_ORDER_AMOUNT:
        warning_min_amount = False
    else:
        warning_min_amount = True

    list_amounts = [(sum(cost_list.values())),
                    int(constants.MINIMUM_ORDER_AMOUNT - sum(cost_list.values()))]

    return render(
        request,
        'cart.html',
        context={
            'order_form': order_form,
            'id_list': id_list,
            'products_in_cart': products_in_cart,
            'cost_list': cost_list,
            'warning_min_amount': warning_min_amount,
            'list_amounts': list_amounts,
        }
    )


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


def remove_product_from_cart(request, product_id):
    product = request.session["cart"]
    del product[product_id]
    request.session['cart'] = product
    return HttpResponseRedirect(request.GET['next'])


def remove_one_copy(request, product_id):
    request.session['cart'][product_id] -= 1
    return HttpResponseRedirect(request.GET['next'])


def send_order(request):
    form = OrderForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect(request)

    form_data = {}
    for key, value in form.cleaned_data.items():
        if value:
            form_data[key] = value

    obj = OrderList.objects.create(
        cost=float(request.GET['cost']),
        address=form_data['address'],
        customer=form_data.get('customer'),
        customer_phone=form_data.get('customer_phone')
    )

    if request.user.is_authenticated:
        obj.customer_id = request.user.id
        obj.save()

    for name, count in request.session["cart"].items():
        ProductListForOrder.objects.create(orderlist_id=obj.id,
                                           product_id=name,
                                           count=count)
    del request.session["cart"]

    return redirect('/allhere.ru/cart')
