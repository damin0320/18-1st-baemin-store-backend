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


class ApplyCouponView(View):
    @auth_check
    @transaction.atomic()
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user_id    = request.user.id
            product_id = data['product_id']

            user_coupons     = UserCoupon.objects.filter(user_id = user_id)
            user_coupon_list = [user_coupon.coupon_id for user_coupon in user_coupons]

            sub_category             = Product.objects.get(id=product_id).sub_category
            sub_category_coupons     = sub_category.couponsubcategory_set.all()
            sub_category_coupon_list = [sub_category_coupon.coupon_id for sub_category_coupon in sub_category_coupons]

            result = []
            for i in user_coupon_list:
                if i in sub_category_coupon_list:
                    result.append(i)
            
            coupon_name = []
            for j in result:
                coupon = Coupon.objects.get(id=j)
                coupon_name.append(coupon.name)
            
            return JsonResponse({'message' : 'SUCCESS', 'coupon_name' : coupon_name}, status=201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)                
            