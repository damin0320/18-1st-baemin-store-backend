import json

from django.views import View
from django.http  import JsonResponse

from .models        import WishList
from product.models import Product, ProductOption, Option, DiscountRate
from user.models    import User

class WishListView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        product        = Product.objects.get(name=['name'])
        user           = User.objects.get(username=['username'])
        product_option = ProductOption.objects.get(id=['id'])
        # id 값
        
        wishlist = WishList.objects.create(
            quantity       = data['quantity'],
            product        = product,
            user           = user,
            product_option = product_option
        )
        
        return JsonResponse({'message' : 'SUCCESS'}, status=200)
