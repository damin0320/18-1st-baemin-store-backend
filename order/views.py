import json
from json import JSONDecodeError

from django.views import View
from django.http  import JsonResponse

from .models        import Order, OrderStatus, Cart
from product.models import Product, ProductOption

PRODUCT_OPTION_ID = 1
PRODUCT_ID = 5
QUANTITY = 2
USER_ID = 2


class CartView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            user_id    = USER_ID
            product_id = data['product_id']
            quantity   = data['quantity'] if not data['quantity'] == 0 else None
            options    = data['options']

            for option in options:
                product_option_id       = option['product_option_id']
                product_option_quantity = option['product_option_quantity']

            before_purchase, is_created = OrderStatus.objects.get_or_create(id=1, status='구매전')

            order = Order.objects.create(user_id=user_id, order_status=before_purchase)

            # product_option_id 없을 때 처리
            cart, is_created = Cart.objects.get_or_create(
                                                          quantity          = quantity,
                                                          order             = order,
                                                          product_id        = product_id,
                                                          product_option_id = product_option_id
                                                        )
            if not is_created:
                cart.quantity += quantity

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
