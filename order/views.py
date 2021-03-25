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
            