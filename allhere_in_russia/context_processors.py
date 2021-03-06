from .forms import ApplicationForOrderingForm, CardApplicationForm, ForLandlordsForm, ForLeaseHoldersForm
from .models import Shops
from shop_allhere import settings


def request(request):
    shops_list = Shops.objects.all()
    current_store = Shops.objects.get(id=request.session['shop'])
    city_list = shops_list.distinct('city').order_by('city')
    return {
        'API_KEY_YANDEX_GEOCODER': settings.API_KEY_YANDEX_GEOCODER,
        'application_for_ordering_form': ApplicationForOrderingForm(),
        'card_application_form': CardApplicationForm(),
        'for_landlords_form': ForLandlordsForm(),
        'for_lease_holders_form': ForLeaseHoldersForm(),
        'shops_list': shops_list,
        'current_store': current_store,
        'city_list': city_list,
    }
