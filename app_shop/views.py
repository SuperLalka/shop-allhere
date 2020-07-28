from django.shortcuts import render
from django.views import generic

from .models import SubPagesArticle


def index(request):
    return render(
        request,
        'index.html'
    )


class SubpageAboutCompanyView(generic.DetailView):
    model = SubPagesArticle
    slug_field = 'address'
    slug_url_kwarg = 'address'

    def get_template_names(self):
        return 'subpage_allhere_in_russia/%s.html' % self.object.section
