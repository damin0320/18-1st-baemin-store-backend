import json
import bcrypt
import jwt
import re
from json import JSONDecodeError

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

from .models          import User, Coupon, UserCoupon
from product.models   import SubCategory, CouponSubCategory
from my_settings      import SECRET_KEY, HASHING_ALGORITHM
from order.models   import WishList
from product.models import Product, ProductOption, Option, DiscountRate
from my_settings import SECRET_KEY, HASHING_ALGORITHM
from utils.decorators import auth_check, user_check


class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            user     = User.objects.get(username=data['username'])
            password = data['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'user_id' : user.id}, SECRET_KEY, algorithm=HASHING_ALGORITHM)
                return JsonResponse({'token' : token, 'message':'SUCCESS'}, status=200)
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'USER_DOES_NOT_EXIST'}, status=401)
        

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            name             = data['name']
            username         = data['username']
            email            = data['email']
            phone_number     = data['phone_number']
            password         = data['password']
            address          = data['address']
            postal_code      = data['postal_code']
            detailed_address = data.get('detailed_address', None)

            if not name or not username or not email or not password or not username or not address or not postal_code:
                return JsonResponse({'message': 'EMPTY_VALUE'}, status=400)

            p_name         = re.compile(r'^[가-힣a-zA-Z]{2,20}$')
            p_username     = re.compile(r'^[a-zA-Z0-9_-]{3,50}$')
            p_email        = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z-.]+$')
            p_phone_number = re.compile(r'^[0-9]{11}$')
            p_password     = re.compile(r'^(?=.*[!-/:-@])(?!.*[ㄱ-ㅣ가-힣]).{8,20}$')

            if not p_name.match(name):
                return JsonResponse({'message': 'INVALID_NAME_FORMAT'}, status=400)
            if not p_username.match(username):
                return JsonResponse({'message': 'INVALID_USERNAME_FORMAT'}, status=400)
            if not p_email.match(email):
                return JsonResponse({'message': 'INVALID_EMAIL_FORMAT'}, status=400)
            if not p_password.match(password):
                return JsonResponse({'message': 'INVALID_PASSWORD_FORMAT'}, status=400)
            if not p_phone_number.match(phone_number):
                return JsonResponse({'message': 'INVALID_PHONE_NUMBER_FORMAT'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'EXISTING_USERNAME'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'EXISTING_EMAIL'}, status=400)
            if User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'message': 'EXISTING_PHONE_NUMBER'}, status=400)

            hashed_pw         = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_pw = hashed_pw.decode('utf-8')

            User.objects.create(
                name             = name,
                username         = username,
                password         = decoded_hashed_pw,
                email            = email,
                phone_number     = phone_number,
                address          = address,
                postal_code      = postal_code,
                detailed_address = detailed_address
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)


class CouponRegistryView(View):
    @transaction.atomic
    @auth_check
    def post(self, request):
        try:
            data           = json.loads(request.body)
            name           = data['name']
            discount_price = data['discount_price']
            issue_date     = data['issue_date']
            expire_date    = data['expire_date']
            coupons = Coupon.objects.create(
                name                = name,
                discount_price      = discount_price,
                issue_date          = issue_date,
                expire_date         = expire_date
            )
            coupon = Coupon.objects.get(name=data['name'])
            sub_categories   = SubCategory.objects.filter(name__in=data['sub_category_name'])
            for sub_category in sub_categories:
                coupon_sub_category = CouponSubCategory.objects.create(
                    coupon=coupon, 
                    sub_category=sub_category
                    )
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)      


class UserCouponView(View):
    @transaction.atomic
    @auth_check    
    def post(self, request):
        try:
            data     = json.loads(request.body)
            coupon   = Coupon.objects.get(id=data['coupon_id']).id
            user     = request.user.id
            quantity = data['quantity']

            
            user_coupon, is_created = UserCoupon.objects.get_or_create(
            coupon_id = coupon,
            user_id   = user,
            defaults  = {'quantity' : quantity}
            )
            if not is_created:
                user_coupon.quantity += data['quantity']
                user_coupon.save()
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
                      
                    
class WishListView(View):
    @auth_check
    @transaction.atomic
    def post(self, request):
        try:
            user_id = request.user.id
            selected_products = json.loads(request.body)['selected_products']
            if not selected_products:
                return JsonResponse({'message': 'OPTION_NOT_SELECTED'}, status=400)

            for selected_product in selected_products:
                product_id              = selected_product['product_id']
                quantity                = selected_product['quantity']
                product_option_id       = selected_product['product_option_id']
                product_option_quantity = selected_product['product_option_quantity']            

                if product_option_id:
                    wishlist, is_created = WishList.objects.get_or_create(
                        product_id        = product_id,
                        product_option_id = product_option_id,
                        user_id           = user_id,
                        defaults          = {'quantity': product_option_quantity}
                        )
                    if not is_created:
                        wishlist.quantity += product_option_quantity
                        wishlist.save()
                else:
                    wishlist, is_created = WishList.objects.get_or_create(
                        product_id = product_id,
                        user_id    = user_id,
                        defaults   = {'quantity': quantity}
                        )

                    if not is_created:
                        wishlist.quantity += quantity
                        wishlist.save()      
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)  

    @auth_check
    def get(self, request):
        wishlists = WishList.objects.filter(user=request.user)
        results = [{
            'point'             : wishlist.user.point,                
            'quantity'          : wishlist.quantity,
            'user_id'           : wishlist.user.id,
            'product_option_id' : wishlist.product_option.id if wishlist.product_option else '',
            'product_id'        : wishlist.product_id,
            'product_name'      : wishlist.product.name,
            'product_thumnail'  : wishlist.product.thumbnail_image_url,
            'product_price'     : wishlist.product.price if not wishlist.product_option\
                                    else wishlist.product.price + wishlist.product_option.additional_price ,
            'total_price'       : wishlist.quantity * wishlist.product.price if not wishlist.product_option\
                                    else wishlist.quantity * (wishlist.product.price + wishlist.product_option.additional_price),
            'product_option_classification': wishlist.product_option.option.classification if wishlist.product_option else '',
            'product_option_name'          : wishlist.product_option.option.name if wishlist.product_option else ''
            } for wishlist in wishlists]

        return JsonResponse({'results' : results}, status=200)
