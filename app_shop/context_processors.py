from .forms import AuthorizationForm, RegistrationForm, SearchForm, SubscriptionForm
from shop_allhere import settings


def request(request):
    return {
        'API_KEY_YANDEX_GEOCODER': settings.API_KEY_YANDEX_GEOCODER,
        'authorization_form': AuthorizationForm(),
        'registration_form': RegistrationForm(),
        'search_form': SearchForm(),
        'user_mail_form': SubscriptionForm(),
    }
