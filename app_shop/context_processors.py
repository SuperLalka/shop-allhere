from .forms import AuthorizationForm, RegistrationForm, SearchForm, SubscriptionForm
from shop_allhere import settings


def request(request):
    authorization_form = AuthorizationForm()
    registration_form = RegistrationForm()
    search_form = SearchForm()
    user_mail_form = SubscriptionForm()
    return {
        'authorization_form': authorization_form,
        'registration_form': registration_form,
        'search_form': search_form,
        'user_mail_form': user_mail_form,
        'API_KEY_YANDEX_GEOCODER': settings.API_KEY_YANDEX_GEOCODER,
    }
