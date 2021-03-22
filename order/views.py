import json

from django.views import View
from django.http  import JsonResponse

from .models        import WishList
from product.models import Product, ProductOption, Option, DiscountRate
from user.models    import User

class WishListView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        product = Product.objects.get(id=data['product_id'])
        user    = User.objects.get(username=data['username'])
        
        
        wishlist = WishList.objects.create(
            quantity          = data['quantity'],
            product           = product,
            user              = user,
            product_option_id = data['product_option_id']
        )
        
        return JsonResponse({'message' : 'SUCCESS'}, status=200)