import json
from json import JSONDecodeError

from django.db       import transaction, IntegrityError
from django.db.utils import DataError
from django.views    import View
from django.http     import JsonResponse

from .models import Product, Category, SubCategory, Option, ProductOption, DiscountRate, BookDescription, ProductDescription


# TODO: Input filtering logic (type, length ...)
class ProductView(View):
    @transaction.atomic
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            category_name         = data['category_name']
            sub_category_name     = data['sub_category_name']
            product_name          = data['product_name']
            price                 = data['price']
            thumbnail             = data['thumbnail']
            images                = data['images']
            stock                 = data['stock']
            discount_rate         = data.get('discount_rate', 0)
            option_classification = data.get('option_classification', None)
            
            category     = Category.objects.get_or_create(name=category_name)[0]
            sub_category = SubCategory.objects.get_or_create(name=sub_category_name, category=category)[0]
            product      = Product.objects.create(
                                                  sub_category        = sub_category,
                                                  name                = product_name,
                                                  price               = price,
                                                  thumbnail_image_url = thumbnail,
                                                  stock               = stock
                                                )
            
            if sub_category == 'book':
                publisher  = data['publisher']
                total_page = data['total_page']
                size_mm    = data.get('size_mm', None)

                BookDescription.objects.create(
                                               product    = product,
                                               title      = product_name,
                                               publisher  = publisher,
                                               size_mm    = size_mm,
                                               total_page = total_page
                                            )
            else:    
                material            = data.get('material', None)
                size_cm             = data.get('size_cm', None)
                manufacture_country = data.get('manufacture_country', None)
                caution             = data.get('caution', None)

                ProductDescription.objects.create(
                                                  product             = product,
                                                  name                = product_name,
                                                  material            = material,
                                                  size_cm             = size_cm,
                                                  manufacture_country = manufacture_country,
                                                  caution             = caution
                                                )

            if option_classification:
                options = data['options']
                for option in options:
                    option_obj = Option.objects.create(
                                                       classification = option_classification,
                                                       name           = option['option_name']
                                                    )

                    ProductOption.objects.create(
                                                 sub_category     = sub_category,
                                                 product          = product,
                                                 stock            = option['option_stock'],
                                                 additional_price = option['additional_price'],
                                                 option           = option_obj
                                            )

            DiscountRate.objects.create(product=product, rate=discount_rate)
            return JsonResponse({'message': 'SUCCESS'}, status=201)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except IntegrityError:
            return JsonResponse({'message': 'INTEGRITY_ERROR'}, status=400)
        except DataError:
            return JsonResponse({'message': 'DATA_ERROR'}, status=400)
