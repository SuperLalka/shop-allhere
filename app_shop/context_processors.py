from .forms import SearchForm


def request(request):
    search_form = SearchForm()
    return {
        'search_form': search_form,
    }
