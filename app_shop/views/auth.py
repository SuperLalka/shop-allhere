from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from app_shop.forms import AuthorizationForm, RegistrationForm
from app_shop.models import OrderList


def authentication(request):
    if request.method != 'POST':
        return render(request, 'authentication.html')

    form = AuthorizationForm(request.POST)
    if not form.is_valid():
        return render(request, 'authentication.html', context={'authorization': True, 'form': form})

    user = authenticate(request, **form.cleaned_data)
    if user is None:
        return render(request, 'authentication.html', context={'authorization': True, 'form': form})
    login(request, user)

    return redirect('app_shop:user_account')


def logout(request):
    auth_logout(request)
    return redirect('app_shop:user_account')


def registration(request):
    form = RegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, 'authentication.html', context={'form': form})

    form.cleaned_data.pop('password_check')
    User.objects.create_user(**form.cleaned_data)
    return render(request, 'authentication.html', context={'authorization': True})


def user_account(request):
    shopping_list = OrderList.objects.filter(customer_id=request.user.id)
    return render(request, 'user_account.html', context={'shopping_list': shopping_list})
