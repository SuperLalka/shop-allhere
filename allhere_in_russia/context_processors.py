from .forms import ApplicationForOrderingForm, CardApplicationForm, ForLandlordsForm, ForLeaseHoldersForm
from .models import Shops
from shop_allhere import settings


def request(request):
    application_for_ordering_form = ApplicationForOrderingForm()
    card_application_form = CardApplicationForm()
    for_landlords_form = ForLandlordsForm()
    for_lease_holders_form = ForLeaseHoldersForm()
    shops_list = Shops.objects.all()
    city_list = sorted(set([item.city for item in Shops.objects.all()]))
    return {
        'application_for_ordering_form': application_for_ordering_form,
        'card_application_form': card_application_form,
        'for_landlords_form': for_landlords_form,
        'for_lease_holders_form': for_lease_holders_form,
        'shops_list': shops_list,
        'API_KEY_YANDEX_GEOCODER': settings.API_KEY_YANDEX_GEOCODER,
        'city_list': city_list,
    }
