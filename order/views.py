import json

from django.db       import transaction
from django.db.utils import DataError
from django.views import View
from django.http  import JsonResponse

from product.models      import (
                          Category, SubCategory, Product,
                          ProductImage, Option, ProductOption
                        )
from user.models      import User, Coupon, UserCoupon
from order.models     import Order
from utils.decorators import auth_check


class ApplyCoupon(View):
    @auth_check
    @transaction.atomic()
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user_id    = request.user.id
            product_id = data['product_id']
            
            sub_category         = Product.objects.get(id=product_id).sub_category
            sub_category_coupons = sub_category.couponsubcategory_set.all()
            
            user_coupons = UserCoupon.objects.filter(user_id = user_id)
            
                
           return JsonResponse({'message' : 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)                
            