import json
import decimal
from json import JSONDecodeError

from django.db       import transaction, IntegrityError
from django.db.utils import DataError
from django.views import View
from django.http  import JsonResponse

from .models      import (
                          Category, SubCategory, Product,
                          ProductImage, ProductDescription, BookDescription,
                          DiscountRate, Option, ProductOption,
                          Review, ProductInquiry
                        )
from user.models  import User
from order.models import Order


class ProductView(View):
    def get(self, request, product_id):
        try:            
            product = Product.objects.get(id=product_id)

            product_name      = product.name
            product_price     = float(product.price)
            product_thumbnail = product.thumbnail_image_url
            product_stock     = product.stock

            discount_rate    = float(DiscountRate.objects.get(product=product).rate) * 100
            discounted_price = product_price - product_price * (discount_rate / 100)

            product_images   = ProductImage.objects.filter(product=product)
            products_options = ProductOption.objects.filter(product=product)

            category_name = product.sub_category.category.name

            if category_name == '책':
                book_description = BookDescription.objects.get(product=product)

                detailed_description = {
                                        'title'     : book_description.title,
                                        'publisher' : book_description.publisher,
                                        'size_mm'   : book_description.size_mm,
                                        'total_page': book_description.total_page
                                    }
            else:
                product_description = ProductDescription.objects.get(product=product)

                detailed_description = {
                                        'name'               : product_description.name,
                                        'material'           : product_description.material,
                                        'size_cm'            : product_description.size_cm,
                                        'manufacture_country': product_description.manufacture_country,
                                        'caution'            : product_description.caution
                                        }           

            product_inquiries = ProductInquiry.objects.filter(product=product)

            # TODO: add review contents
            results = {
                        'category_name'    : category_name,
                        'product_name'     : product_name,
                        'product_price'    : product_price,
                        'discount_rate'    : int(discount_rate),
                        'discounted_price' : int(discounted_price),
                        'product_thumbnail': product_thumbnail,
                        'product_stock'    : product_stock,
                        'images_list'      : [product_image.image_url for product_image in product_images],
                        'options_list'     : [
                                                {
                                                 'option_name'            : product_option.option.name,
                                                 'option_classification'  : product_option.option.classification,
                                                 'option_stock'           : product_option.stock,
                                                 'option_additional_price': float(product_option.additional_price),
                                                 'product_option_id'      : product_option.id
                                                } for product_option in products_options],
                        'detailed_description': detailed_description,
                        'inquiries_list'      : [
                                                {
                                                'product_inquiry_content' : product_inquiry.content,
                                                'product_inquiry_username': product_inquiry.user.username
                                                } for product_inquiry in product_inquiries],
                        'reviews_list': ''
                        }
            
            return JsonResponse(results, status=200) 

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXIST'}, status=404)
        except DiscountRate.DoesNotExist:
            return JsonResponse({'message': 'DISCOUNTRATE_DOES_NOT_EXIST'}, status=404)
        except BookDescription.DoesNotExist:
            return JsonResponse({'message': 'BOOKDESCRIPTION_DOES_NOT_EXIST'}, status=404)
        except ProductDescription.DoesNotExist:
            return JsonResponse({'message': 'PRODUCTDESCRIPTION_DOES_NOT_EXIST'}, status=404)


# TODO: Input filtering logic (type, length ...)
class ProductRegistryView(View):
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

            category    , _ = Category.objects.get_or_create(name=category_name)
            sub_category, _ = SubCategory.objects.get_or_create(name=sub_category_name, category=category)
            product         = Product.objects.create(
                                                     sub_category        = sub_category,
                                                     name                = product_name,
                                                     price               = price,
                                                     thumbnail_image_url = thumbnail,
                                                     stock               = stock
                                                )
            
            for image in images:
                ProductImage.objects.create(product=product, image_url=image)
                
            if sub_category.name == '책':
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
                    option_obj, _ = Option.objects.get_or_create(
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
