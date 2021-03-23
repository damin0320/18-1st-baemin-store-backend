import json
from json import JSONDecodeError

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

from .models          import Order, OrderStatus, Cart
from product.models   import Product, ProductOption
from utils.decorators import user_check, auth_check


class CartView(View):
    @transaction.atomic
    @auth_check
    def post(self, request):
        try:
            result     = json.loads(request.body)['results']
            product_id = results[0]['product_id']

            before_purchase, _ = OrderStatus.objects.get_or_create(id=1, status='구매전')
            order, _           = Order.objects.get_or_create(user=request.user, order_status=before_purchase)
            product            = Product.objects.get(id=product_id)
            
            for result in results:
                quantity                = result['quantity']
                product_option_id       = result['product_option_id']
                product_option_quantity = result['product_option_quantity']

                if product_option_id:
                    cart, is_created = Cart.objects.get_or_create(
                                                                  product           = product,
                                                                  order             = order,
                                                                  product_option_id = product_option_id,
                                                                  defaults          = {'quantity': product_option_quantity}
                                                                )
                    if not is_created:
                        cart.quantity += option['product_option_quantity']
                        cart.save()
                else:
                    cart, is_created = Cart.objects.get_or_create(
                                                                  product  = product,
                                                                  order    = order,
                                                                  defaults = {'quantity': quantity}
                                                                )
                    if not is_created:
                        cart.quantity += quantity
                        cart.save()
                return JsonResponse({'message': 'SUCCESS'}, status=201)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXIST'}, status=404)

    @auth_check
    def get(self, request):
        try:
            order = Order.objects.get(user=request.user, order_status_id=1)

            carts     = order.cart_set.all()
            cart_list = [{'product_id': cart.product.id,
                          'product_thumbnail': cart.product.thumbnail_image_url,
                          'product_name': cart.product.name,
                          'quantity': cart.quantity,
                          'product_price': float(cart.product.price) if not cart.product_option else float(cart.product.price + cart.product_option.additional_price),
                          'total_price': cart.quantity * float(cart.product.price) if not cart.product_option else cart.quantity * float(cart.product.price + cart.product_option.additional_price),
                          'product_option_id': cart.product_option_id,
                          'product_option_classification': cart.product_option.option.classification,
                          'product_option_name': cart.product_option.option.name} for cart in carts]
            return JsonResponse({'results': cart_list}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        