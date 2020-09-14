from .forms import ApplicationForOrderingForm, CardApplicationForm, ForLandlordsForm, ForLeaseHoldersForm
from .models import Shops
from shop_allhere import settings


def request(request):
    shops_list = Shops.objects.all()
    city_list = shops_list.values_list('city', flat=True).distinct().order_by('city')
    return {
        'API_KEY_YANDEX_GEOCODER': settings.API_KEY_YANDEX_GEOCODER,
        'application_for_ordering_form': ApplicationForOrderingForm(),
        'card_application_form': CardApplicationForm(),
        'for_landlords_form': ForLandlordsForm(),
        'for_lease_holders_form': ForLeaseHoldersForm(),
        'shops_list': shops_list,
        'city_list': city_list,
    }
