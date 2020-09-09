from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from app_shop.forms import AuthorizationForm, RegistrationForm
from app_shop.models import OrderList


def authentication(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        if not form.is_valid():
            return render(request, 'authentication.html', context={'authorization': True, 'form': form})

        user = authenticate(request,
                            username=form.cleaned_data['user_name'],
                            password=form.cleaned_data['user_password'])
        if user is not None:
            login(request, user)
            return redirect('app_shop:user_account')
        else:
            return render(request, 'authentication.html', context={'authorization': True, 'form': form})
    else:
        return render(request, 'authentication.html')


def logout_from_profile(request):
    logout(request)
    return redirect('app_shop:user_account')


def registration(request):
    form = RegistrationForm(request.POST)
    if not form.is_valid():
        return render(request, 'authentication.html', context={'form': form})

    User.objects.create_user(form.cleaned_data['user_name'],
                             form.cleaned_data['user_email'],
                             form.cleaned_data['user_password'])
    return render(request, 'authentication.html', context={'authorization': True})


def user_account(request):
    shopping_list = OrderList.objects.filter(customer_id=request.user.id)
    return render(request, 'user_account.html', context={'shopping_list': shopping_list})
