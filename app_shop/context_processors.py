from .forms import SearchForm, SubscriptionForm


def request(request):
    search_form = SearchForm()
    user_mail_form = SubscriptionForm()
    return {
        'search_form': search_form,
        'user_mail_form': user_mail_form,
    }
