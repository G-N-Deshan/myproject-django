from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class CartTransferMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                from .models import Cart
                cart = Cart.objects.filter(user=request.user).first()
                if cart:
                    logger.debug(f"User {request.user.username} has {cart.get_item_count()} items in cart")
            except Exception as e:
                logger.error(f"Error in CartTransferMiddleware: {str(e)}")
        return response

class ErrorHandlingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger.error(f"Exception: {str(exception)}", exc_info=True)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': 'An error occurred. Please try again.'
            }, status=500)

        return None
