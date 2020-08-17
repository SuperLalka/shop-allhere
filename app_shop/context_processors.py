from .forms import ApplicationForOrderingForm, CardApplicationForm, ForLandlordsForm, ForLeaseHoldersForm, SearchForm, SubscriptionForm
from .models import Shops, ProductClassification
from shop_allhere import settings


def request(request):
    application_for_ordering_form = ApplicationForOrderingForm()
    card_application_form = CardApplicationForm()
    for_landlords_form = ForLandlordsForm()
    for_lease_holders_form = ForLeaseHoldersForm()
    search_form = SearchForm()
    user_mail_form = SubscriptionForm()
    shops_list = Shops.objects.all()
    city_list = sorted(set([item.city for item in Shops.objects.all()]))
    highest_categories = ProductClassification.objects.filter(highest_category=True)
    list_categories = ProductClassification.objects.all().exclude(highest_category=True)
    return {
        'application_for_ordering_form': application_for_ordering_form,
        'card_application_form': card_application_form,
        'for_landlords_form': for_landlords_form,
        'for_lease_holders_form': for_lease_holders_form,
        'search_form': search_form,
        'user_mail_form': user_mail_form,
        'shops_list': shops_list,
        'API_KEY_YANDEX_GEOCODER': settings.API_KEY_YANDEX_GEOCODER,
        'city_list': city_list,
        'highest_categories': highest_categories,
        'list_categories': list_categories,
    }
