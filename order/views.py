import json
from json import JSONDecodeError

from django.views import View
from django.http  import JsonResponse
from django.db    import transaction

from .models        import WishList
from product.models import Product, ProductOption, Option, DiscountRate
from user.models    import User

class WishListView(View):
    @transaction.atomic
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            user = User.objects.get(username=data['username'])
            
            wishlist, is_created = WishList.objects.get_or_create(
                
            quantity          = data['quantity'],
            product_id        = data['product_id'],
            user              = user,
            product_option_id = data['product_option_id'],
            )

                # wishlist, is_created = WishList.objects.get_or_create(
                # quantity   = data['quantity'],
                # product_id = data['product_id'],
                # user       = user,
                # options    = data['product_option_id', 'product_option_quantity'],
                # )
            if is_created is False:
                wishlist.quantity += data['quantity']
                wishlist.save()
            else:
                return wishlist
                
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except WishList.DoesNotExist:
            return JsonResponse({'message' : 'WISHLIST_DOES_NOT_EXIST'}, status=404)    

    
    def get(self, request):
        wishlists = WishList.objects.filter(user_id=3)
        try:
            result = [dict(
                point             = user.point,                
                quantity          = wishlist.quantity,
                user_id           = wishlist.user.id,
                product_option_id = wishlist.product_option.id,
                product_id        = product.id,
                product           = product.name,
                product_thumnail  = product.thumbnail_image_url,
                price             = product.price,
                ) for wishlist in wishlists]
                
                # my_dict = dict(
                #     quantity          = wishlist.quantity,
                #     product_id        = product.id,
                #     product           = product.name,
                #     product_thumnail  = product.thumbnail_image_url,
                #     user_id           = wishlist.user.id,
                #     product_option_id = wishlist.product_option.id,
                #     price             = product.price,
                #     point             = user.point
                # )
                # result.append(my_dict)
            return JsonResponse({'result' : result}, status=200)
        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except WishList.DoesNotExist:
            return JsonResponse({'message' : 'WISHLIST_DOES_NOT_EXIST'}, status=404)