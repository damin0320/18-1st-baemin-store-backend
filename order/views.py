import json
from json import JSONDecodeError

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

from .models          import Order, OrderStatus, Cart
from product.models   import Product, ProductOption
from utils.decorators import user_check, auth_check

USER_ID = 2


class CartView(View):
    @transaction.atomic
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            user_id    = USER_ID
            product_id = data['product_id']
            quantity   = data['quantity'] if not data['quantity'] == 0 else None
            options    = data['options']

            before_purchase, _ = OrderStatus.objects.get_or_create(id=1, status='구매전')
            order, _           = Order.objects.get_or_create(user_id=user_id, order_status=before_purchase)
            if options:
                for option in options:
                    cart, is_created = Cart.objects.get_or_create(
                                                                  product_id        = product_id,
                                                                  order             = order,
                                                                  product_option_id = option['product_option_id'],
                                                                  defaults          = {'quantity': option['product_option_quantity']}
                                                                )
                    if not is_created:
                        cart.quantity += option['product_option_quantity']
                        cart.save()

                return JsonResponse({'message': 'SUCCESS'}, status=201)

            cart, is_created = Cart.objects.get_or_create(
                                                            product_id = product_id,
                                                            order      = order,
                                                            defaults={'quantity': quantity}
                                                        )
            if not is_created:
                cart.quantity += quantity
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    def get(self, request):
        pass
        