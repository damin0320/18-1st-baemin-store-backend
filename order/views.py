import json
from json import JSONDecodeError

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

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

            before_purchase, _      = OrderStatus.objects.get_or_create(id=1, status='구매전')
            order, is_order_created = Order.objects.get_or_create(user_id=user_id, order_status=before_purchase)

            if options:
                for option in options:
                    cart, _ = Cart.objects.get_or_create(
                                                         quantity          = option['product_option_quantity'],
                                                         product_option_id = option['product_option_id'],
                                                         order             = order,
                                                         product_id        = product_id
                                                    )
###### 옵션 quantity 별로 추가

            if not is_order_created:
                cart.quantity += quantity

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
