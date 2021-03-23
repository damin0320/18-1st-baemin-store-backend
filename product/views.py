import json
from json import JSONDecodeError

from django.views import View
from django.http  import JsonResponse

from .models import (
                     Category, SubCategory, Product,
                     ProductImage, ProductDescription, BookDescription,
                     DiscountRate, Option, ProductOption,
                     Review, ProductInquiry
                )
from user.models  import User
from order.models import Order


class CategoryView(View):
    def get(self, request, category_name):
        try:
            category       = Category.objects.get(name=category_name)
            sub_categories = SubCategory.objects.filter(category=category)

            products_obj_list = list()
            for sub_category in sub_categories:
                products = Product.objects.filter(sub_category=sub_category)
                products_obj_list += list(products)
            
            products_list = list()
            for product in products_obj_list:
                discount_rate    = float(DiscountRate.objects.get(product=product).rate * 100)
                discounted_price = float(product.price) - (float(product.price) * (discount_rate / 100))

                product_dict = {
                                'product_id'       : product.id,
                                'product_name'     : product.name,
                                'product_price'    : float(product.price),
                                'product_thumbnail': product.thumbnail_image_url,
                                'discount_rate'    : discount_rate,
                                'discounted_price' : discounted_price
                                }
                products_list.append(product_dict)
            return JsonResponse({'results': products_list}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)    
        except Category.DoesNotExist:
            return JsonResponse({'message': 'CATEGORY_DOES_NOT_EXIST'}, status=404)
        except DiscountRate.DoesNotExist:
            return JsonResponse({'message': 'DISCOUNTRATE_DOES_NOT_EXIST'}, status=404)
