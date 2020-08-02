from django.shortcuts import render
from django.views import generic

from .forms import ApplicationForOrderingForm
from .models import Shops, SubPagesArticle


def index(request, **kwargs):
    template_name = 'index.html'
    if kwargs:
        template_name = '%s.html' % kwargs['page']
        if kwargs['page'] is 'for_wholesalers':
            application_for_ordering_form = ApplicationForOrderingForm()
            return render(
                request,
                template_name,
                context={'application_for_ordering_form': application_for_ordering_form}
            )
    return render(
        request,
        template_name
    )


class SubpageAboutCompanyView(generic.DetailView):
    model = SubPagesArticle
    slug_field = 'address'
    slug_url_kwarg = 'address'

    def get_template_names(self):
        if self.object.uniq_template is True:
            return 'subpage_allhere_in_russia/uniq/%s.html' % self.object.address
        return 'subpage_allhere_in_russia/%s.html' % self.object.section


class ShopDetailView(generic.DetailView):
    model = Shops
    template_name = 'subpage_allhere_in_russia/uniq/shop_detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'
