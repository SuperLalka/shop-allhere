from .forms import SearchForm, SubscriptionForm
from .models import Shops
from shop_allhere import settings


def request(request):
    search_form = SearchForm()
    user_mail_form = SubscriptionForm()
    shops_list = Shops.objects.all()
    city_list = sorted(set([item.city for item in Shops.objects.all()]))
    return {
        'search_form': search_form,
        'user_mail_form': user_mail_form,
        'shops_list': shops_list,
        'API_KEY_YANDEX_GEOCODER': settings.API_KEY_YANDEX_GEOCODER,
        'city_list': city_list,
    }
