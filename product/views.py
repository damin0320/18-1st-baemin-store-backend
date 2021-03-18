import json

from django.views import View
from django.http  import JsonResponse

from .models import Category, SubCategory, Product, Option, DiscountRate, ProductOption

class ProductView(View):
    def get(self, request):
        products        = Product.objects.all()
        options         = Option.objects.filter(name=data['subcategory'])
        product_options = Product.productoption_set
        discount_rates  = Product.discountrate_set
        result = []
        
        for product in products:
            product_dict = {
                'name'              : product.name,
                'thumbnail_imge_url': product.thumbnail_imge_url,
                'price'             : product.price,
            }
        for option in options:
            option_dict = {
                'option' : option.name
            }
        for product_option in product_options:
            product_option_dict = {
                'stock'           : product_option.stock,
                'additional_price': product_option.additional_price
            }
        for discount_rate in discount_rates:
            discount_rate_dict = {
                'rate' : discount_rate.rate
            }
            result.append(product_dict, option_dict, product_option_dict, discount_rate_dict)
        return JsonResponse({"result" : result}, status=200)