from django.utils.deprecation import MiddlewareMixin

from app_shop.models import VisitStatistics
from shop_allhere.constants import DEFAULT_STORE_ID


class CollectingStatistics(MiddlewareMixin):

    def process_response(self, request, response):
        if "/media/" not in request.path:
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
            request.session['shop'] = DEFAULT_STORE_ID

        if not request.session.get('cart', None):
            request.session['cart'] = {}
