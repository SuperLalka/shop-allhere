from django.utils.deprecation import MiddlewareMixin

from allhere_in_russia.models import Shops
from app_shop.models import VisitStatistics
from .constants import DEFAULT_STORE


class CollectingStatistics(MiddlewareMixin):

    def process_response(self, request, response):
        if response.status_code == 302:
            action = None
            if "cart/add_product" in request.path:
                action = 'add_product'
            elif "registration" in request.path:
                action = 'registration'
            elif "subscription" in request.path:
                action = 'subscription'
            VisitStatistics.objects.create(
                url_address=response.url,
                user_id=request.user.id,
                actions=action
            )

        if response.status_code == 200:
            if response.get('url', request.path) not in request.headers.get('Referer', request.path):
                VisitStatistics.objects.create(
                    url_address=request.path,
                    user_id=request.user.id,
                )

        return response


class UserIdentifier(MiddlewareMixin):

    def process_request(self, request):
        if not request.session.get('shop', None):
            default_shop = Shops.objects.filter(city=DEFAULT_STORE).first()
            request.session['shop'] = int(default_shop.id)

        if not request.session.get('cart', None):
            request.session['cart'] = {}
