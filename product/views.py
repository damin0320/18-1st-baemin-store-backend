import json

from django.views import View
from django.http  import JsonResponse

from .models import Category, SubCategory, Product, DiscountRate, Option, ProductOption

class ProductShowInformationView(View):
    def get(self, request):
        productshowinformations = Product.objects.all()
        options                 = Product.product_options.filter(subcategory=data['subcategory'])
        discount_rates          = Product.discountrate.filter(product=data['product'])
        productoptions          = Product.product_options.filter(stock=data['stock'], additional_price=data['additional_price'])

        result = []
        
        for productshowinformation in productshowinformations:
            productshowinformation_dict = {
                'name'               : productshowinformation.name,
                'price'              : productshowinformation.price,
                'thumbnail_image_url': productshowinformation.thumbnail_image_url
            }
        for option in options:
            option_dict = {
                'classification': classification,
                'name'          : name
            }
        for productoption in productoptions:
            productoption_dict = {
                'stock'           : stock,
                'additional_price': additional_price
            }
        for discount_rate in discount_rates:
            discount_rate_dict = {
                'rate' : rate
            }
        result.append(productshowinformation_dict, option_dict, discount_rate_dict)
        return JsonResponse({'result' : result}, status=200)