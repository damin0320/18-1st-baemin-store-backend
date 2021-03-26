import json
from json import JSONDecodeError

from django.views     import View
from django.http      import JsonResponse
from django.db        import transaction
from django.db.models import Q
from django.db.utils  import IntegrityError, DataError

from .models          import Order, OrderStatus, Cart
from user.models      import User, DeliveryAddress, Coupon, UserCoupon
from utils.decorators import user_check, auth_check
from product.models   import (
                          Category, SubCategory, Product,
                          ProductImage, Option, ProductOption
                        )


class StockDoesNotExist(Exception):
    pass


class PointNotEnough(Exception):
    pass


class QuantityZeroError(Exception):
    pass


class CartView(View):
    @auth_check
    def post(self, request):
        try:
            selected_products = json.loads(request.body)['selected_products']
            if not selected_products:
                return JsonResponse({'message': 'OPTION_NOT_SELECTED'}, status=400)

            with transaction.atomic():
                before_purchase, _ = OrderStatus.objects.get_or_create(id=1, status='구매전')
                order, _           = Order.objects.get_or_create(user=request.user, order_status=before_purchase)

                for selected_product in selected_products:
                    product_id              = selected_product['product_id']
                    quantity                = selected_product['quantity']
                    product_option_id       = selected_product['product_option_id']
                    product_option_quantity = selected_product['product_option_quantity']

                    if product_option_id:
                        if product_option_quantity == 0:
                            raise QuantityZeroError

                        cart, is_created = Cart.objects.get_or_create(
                                                                    product_id        = product_id,
                                                                    order             = order,
                                                                    product_option_id = product_option_id,
                                                                    defaults          = {'quantity': product_option_quantity}
                                                                    )
                        if not is_created:
                            cart.quantity += product_option_quantity
                            cart.save()
                    else:
                        if quantity == 0:
                            raise QuantityZeroError

                        cart, is_created = Cart.objects.get_or_create(
                                                                    product_id = product_id,
                                                                    order      = order,
                                                                    defaults   = {'quantity': quantity}
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
        except TypeError:
            return JsonResponse({'message': 'TYPE_ERROR'}, status=400)
        except IntegrityError:
            return JsonResponse({'message': 'INTEGRITY_ERROR'}, status=400)
        except QuantityZeroError:
            return JsonResponse({'message': 'QUANTITY_ZERO_ERROR'}, status=400)


    @auth_check
    def get(self, request):
        """
        order_status_id --> 1 : 구매전 
        order_status_id --> 2 : 결제중
        """
        try:
            order_before_purchase = Order.objects.get(user=request.user, order_status_id=1)
            order_pending_purchase = Order.objects.filter(user=request.user, order_status_id=2).first()

            # 구매전, 결제중(결제페이지 이동했던 상품들) 상품들 모두 장바구니에 담는다.
            # 장바구니 페이지에서 목록 삭제 가능
            carts = list(order_before_purchase.cart_set.all()) + list(order_pending_purchase.cart_set.all())\
                    if order_pending_purchase else list(order_before_purchase.cart_set.all())
                    
            if not carts:
                return JsonResponse({'message': 'CART_IS_EMPTY'}, status=404)

            cart_list = [
                         {'product_id'                   : cart.product.id,
                          'product_thumbnail'            : cart.product.thumbnail_image_url,
                          'product_name'                 : cart.product.name,
                          'quantity'                     : cart.quantity,
                          'stock'                        : cart.product.stock if not cart.product_option else cart.product_option.stock,
                          'product_price'                : float(cart.product.price) if not cart.product_option \
                                                           else float(cart.product.price + cart.product_option.additional_price),
                          'total_price'                  : cart.quantity * float(cart.product.price) if not cart.product_option \
                                                           else cart.quantity * float(cart.product.price + cart.product_option.additional_price),
                          'product_option_id'            : cart.product_option.id if cart.product_option else '',
                          'product_option_classification': cart.product_option.option.classification if cart.product_option else '',
                          'product_option_name'          : cart.product_option.option.name if cart.product_option else '',
                          'order_status'                 : cart.order.order_status.status,
                          'order_id'                     : cart.order_id
                        } for cart in carts]
            return JsonResponse({'results': cart_list}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Order.DoesNotExist:
            return JsonResponse({'message': 'CART_IS_EMPTY'}, status=404)
    
    @auth_check
    def delete(self, request):
        try:
            selected_products = json.loads(request.body)['selected_products']
            if not selected_products:
                return JsonResponse({'message': 'PRODUCT_NOT_SELECTED'}, status=400)
            with transaction.atomic():
                for selected_product in selected_products:
                    if selected_product['product_option_id']:
                        Cart.objects.get(
                                        product_id        = selected_product['product_id'],
                                        product_option_id = selected_product['product_option_id'],
                                        order_id          = selected_product['order_id']
                                    ).delete()
                    else:
                        Cart.objects.get(
                                        product_id = selected_product['product_id'],
                                        order_id   = selected_product['order_id']
                                    ).delete()
            return JsonResponse({'message': 'SUCCESS'}, status=204)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'CART_DOES_NOT_EXIST'}, status=404)
    
    # 장바구니에서 상품을 몇개만 선택할 수 있음
    @auth_check
    def patch(self, request):
        try:            
            selected_products = json.loads(request.body)['selected_products']
            if not selected_products:
                return JsonResponse({'message': 'PRODUCT_NOT_SELECTED'}, status=400)

            with transaction.atomic():
                before_purchase, _  = OrderStatus.objects.get_or_create(id=1, status='구매전')
                pending_purchase, _ = OrderStatus.objects.get_or_create(id=2, status='결제중')

                order_before_purchase, _  = Order.objects.get_or_create(user=request.user, order_status=before_purchase)
                order_pending_purchase, _ = Order.objects.get_or_create(user=request.user, order_status=pending_purchase)

                for selected_product in selected_products:
                    product_id        = selected_product['product_id']
                    product_option_id = selected_product['product_option_id']

                    # 결제중인 상품도 장바구니에 노출되는데, 결제중인 상품을 선택해서 담을 가능성이 있기때문에
                    # get 으로 하면 에러가 나기 때문에 filter로 했음. 
                    if product_option_id:
                        cart = Cart.objects.filter(
                                                product_id        = product_id,
                                                product_option_id = product_option_id,
                                                order             = order_before_purchase
                                                ).first()

                        pending_cart = Cart.objects.filter(
                                                        product_id        = product_id,
                                                        product_option_id = product_option_id,
                                                        order             = order_pending_purchase
                                                        ).first()
                    else:
                        cart = Cart.objects.filter(
                                                product_id = product_id,
                                                order      = order_before_purchase
                                                ).first()

                        pending_cart = Cart.objects.filter(
                                                        product_id = product_id,
                                                        order      = order_pending_purchase
                                                        ).first()
                    if not cart:
                        continue

                    if pending_cart:
                        pending_cart.quantity += cart.quantity
                        pending_cart.save()
                        cart.delete()
                    else:
                        cart.order = order_pending_purchase
                        cart.save()
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'CART_DOES_NOT_EXIST'}, status=404)
    

class OrderView(View):
    @auth_check
    def get(self, request):
        try:
            order_pending_purchase = Order.objects.get(user=request.user, order_status_id=2)
            
            carts = order_pending_purchase.cart_set.all()
            if not carts:
                return JsonResponse({'message': 'PRODUCT_NOT_SELECTED'}, status=404)

            cart_list = [
                         {
                          'product_id'                   : cart.product.id,
                          'order_id'                     : cart.order_id,
                          'product_thumbnail'            : cart.product.thumbnail_image_url,
                          'product_name'                 : cart.product.name,
                          'quantity'                     : cart.quantity,
                          'product_price'                : float(cart.product.price) if not cart.product_option \
                                                           else float(cart.product.price + cart.product_option.additional_price),
                          'total_price'                  : cart.quantity * float(cart.product.price) if not cart.product_option \
                                                           else cart.quantity * float(cart.product.price + cart.product_option.additional_price),
                          'product_option_id'            : cart.product_option.id if cart.product_option else '',
                          'product_option_classification': cart.product_option.option.classification if cart.product_option else '',
                          'product_option_name'          : cart.product_option.option.name if cart.product_option else ''
                        } for cart in carts]
            
            user = User.objects.get(id=request.user.id)
            user_detail = {
                           "name"            : user.name,
                           "phone_number"    : user.phone_number,
                           "email"           : user.email,
                           "delivery_address": user.address,
                           "postal_code"     : user.postal_code,
                           "detailed_address": user.detailed_address,
                           "point"           : user.point
                        }
            
            return JsonResponse({'products': cart_list, 'user': user_detail}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except Order.DoesNotExist:
            return JsonResponse({'message': 'ORDER_DOES_NOT_EXIST'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status=404)


    # TODO: 입력정보 유효성 검사
    @auth_check
    def post(self, request):
        """
        결제시 상품 옵션 재고 및 전체 옵션도 합산해서 깎기
        재고 없으면 에러메시지 보내고 "결제중" -> "구매전" 으로 변경
        결제시 order_status "결제중" -> "배송완료" 로 변경
        """
        try:
            data = json.loads(request.body)

            products    = data['products']
            receiver    = data['receiver']
            user_detail = data['user']

            for k, v in receiver.items():
                if not v:
                    return JsonResponse({'message': 'NECESSARY_INFORMATION_NOT_FILLED, {}'.format(k)}, status=400)
            
            for k, v in user_detail.items():
                if not v:
                    return JsonResponse({'message': 'NECESSARY_INFORMATION_NOT_FILLED, {}'.format(k)}, status=400)

            # 장바구니("구매전")에 담아야 결제페이지 까지 올 수 있기 때문에
            # 이미 order_status 테이블에 "구매전" 이 있을 것이기 때문에 get 으로 처리함

            with transaction.atomic():
                before_purchase          = OrderStatus.objects.get(id=1)
                order_before_purchase, _ = Order.objects.get_or_create(user=request.user, order_status=before_purchase) 

                delivery_done, _    = OrderStatus.objects.get_or_create(id=3, status='배송완료')
                order_delivery_done = Order.objects.create(user=request.user, order_status=delivery_done)

                for product in products:
                    if product['product_option_id']:
                        cart = Cart.objects.get(
                                                product_id        = product['product_id'],
                                                product_option_id = product['product_option_id'],
                                                order_id          = product['order_id']
                                            )
                        if cart.product_option.stock - cart.quantity < 0:
                            raise StockDoesNotExist

                        cart.product_option.stock -= cart.quantity
                        cart.product_option.save()

                        cart.product.stock -= cart.quantity
                        cart.product.save()                        
                    else:
                        cart = Cart.objects.get(
                                                product_id = product['product_id'],
                                                order_id   = product['order_id']
                                            )
                        if cart.product.stock - cart.quantity < 0:
                            raise StockDoesNotExist
                            
                        cart.product.stock -= cart.quantity
                        cart.product.save()

                    cart.order = order_delivery_done
                    cart.save()

                Order.objects.filter(
                                     id           = order_delivery_done.id,
                                     user         = request.user,
                                     order_status = delivery_done).update(
                                                                          receiver_name    = receiver['name'],
                                                                          phone_number     = receiver['phone_number'],
                                                                          delivery_address = receiver['delivery_address'],
                                                                          postal_code      = receiver['postal_code'],
                                                                          detailed_address = receiver['detailed_address'],
                                                                          customor_message = receiver['customor_message']
                                                                        )
                
                if float(request.user.point) < float(user_detail['point_used']):
                    raise PointNotEnough                    

                User.objects.filter(id=request.user.id).update(point=float(request.user.point) - float(user_detail['point_used']) + float(user_detail['point']))

                if user_detail['add_my_address'] == 1:
                    DeliveryAddress.objects.get_or_create(
                                                            user             = request.user, 
                                                            address          = receiver['delivery_address'],
                                                            postal_code      = receiver['postal_code'],
                                                            detailed_address = receiver['detailed_address']
                                                        )
                
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'CART_DOES_NOT_EXIST'}, status=404)
        except StockDoesNotExist:
            cart.order = order_before_purchase
            cart.save()
            return JsonResponse({'message': '{}, 재고가 없습니다.'.format(cart.product.name)}, status=400)
        except PointNotEnough:
            return JsonResponse({'message': 'NOT_ENOUGH_POINT'}, status=400)


class ApplyCouponView(View):
    @auth_check
    def get(self, request, product_id):
        try:
            user_id    = request.user.id
            product = Product.objects.get(id=product_id)

            user_coupons     = UserCoupon.objects.filter(user_id = user_id)
            user_coupon_list = [user_coupon.coupon_id for user_coupon in user_coupons]

            sub_category             = Product.objects.get(id=product_id).sub_category
            sub_category_coupons     = sub_category.couponsubcategory_set.all()
            sub_category_coupon_list = [sub_category_coupon.coupon_id for sub_category_coupon in sub_category_coupons]
            
            coupon_name = [Coupon.objects.get(id=j).name for j in [i for i in user_coupon_list if i in sub_category_coupon_list]]
            
            return JsonResponse({'message' : 'SUCCESS', 'coupon_name' : coupon_name}, status=201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)                
            
