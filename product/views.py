import json
import datetime
from json import JSONDecodeError

from django.views import View
from django.http  import JsonResponse
from django.db        import transaction, IntegrityError
from django.db.utils  import DataError
from django.db.models import Sum

from .models import (
                     Category, SubCategory, Product,
                     ProductImage, ProductDescription, BookDescription,
                     DiscountRate, Option, ProductOption,
                     Review, ProductInquiry
                )
from user.models  import User
from order.models import Order, WishList, Cart

from utils.decorators import user_check
from utils.util       import get_hot_products_querysets


class CategoryView(View):
    @user_check
    def get(self, request, category_name):
        try:
            if not category_name == '전체':
                sub_categories = SubCategory.objects.filter(category__name=category_name)

                products_obj_list = []
                for sub_category in sub_categories:
                    products = Product.objects.filter(sub_category=sub_category)
                    products_obj_list += list(products)
            else:
                products_obj_list = Product.objects.all()
            
            products_list = []
            for product in products_obj_list:
                discount_rate    = float(DiscountRate.objects.get(product=product).rate * 100)
                discounted_price = float(product.price) - (float(product.price) * (discount_rate / 100))
                
                is_in_wishlist   = 1 if WishList.objects.filter(user=request.user, product=product).exists() else 0

                product_dict = {
                                'product_id'       : product.id,
                                'product_name'     : product.name,
                                'product_price'    : float(product.price),
                                'product_thumbnail': product.thumbnail_image_url,
                                'discount_rate'    : discount_rate,
                                'discounted_price' : discounted_price,
                                'stock'            : product.stock,
                                'is_in_wishlist'   : is_in_wishlist,
                                'is_new'           : 1 if product in Product.objects.filter\
                                                    (updated_at__gte=datetime.datetime.today()-datetime.timedelta(days=7))\
                                                    else 0,
                                'is_best': 1 if product in get_hot_products_querysets() else 0,
                                'is_sale': 1 if discount_rate > 0 else 0
                            }
                products_list.append(product_dict)
            return JsonResponse({'results': products_list}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)    
        except Category.DoesNotExist:
            return JsonResponse({'message': 'CATEGORY_DOES_NOT_EXIST'}, status=404)
        except DiscountRate.DoesNotExist:
            return JsonResponse({'message': 'DISCOUNTRATE_DOES_NOT_EXIST'}, status=404)

            
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
                        'product_id'       : product_id,
                        'product_name'     : product_name,
                        'product_price'    : product_price,
                        'discount_rate'    : discount_rate,
                        'discounted_price' : discounted_price,
                        'product_thumbnail': product_thumbnail,
                        'product_stock'    : product_stock,
                        'counts'           : 1,
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
        except TypeError:
            return JsonResponse({'message': 'TYPE_ERROR'}, status=400)



class MainPageView(View):
    @user_check
    def get(self, request):
        try:            
            # 인기상품 상위 4개 구하는 로직
            hot_products = get_hot_products_querysets()[:4]
            hot_products_detail = self.get_product_details(hot_products, request.user)

            # 신상품 8개 구하는 로직, 신상순
            new_products = Product.objects.all().order_by('-created_at')[:8]
            new_products_detail = self.get_product_details(new_products, request.user)

            # 할인상품 8개 구하는 로직, 할인율 10프로 이상, 남은 재고 (stock) 가 많은 상품순대로
            discount_rates = DiscountRate.objects.filter(rate__gte=0.1)
            
            product_querysets = Product.objects.none()
            for discount_rate in discount_rates:
                product_querysets |= Product.objects.filter(id=discount_rate.product_id)  

            sale_products = product_querysets[:8]
            sale_products_detail = self.get_product_details(sale_products, request.user)
            
            results = {
                       'hot_products' : hot_products_detail,
                       'new_products' : new_products_detail,
                       'sale_products': sale_products_detail
                    } 
            return JsonResponse(results, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXIST'}, status=404)

    def get_product_details(self, products, user):
        """
        products : iterable Model objects in list type or QuerySet type
        """
        products_detail = []
        for product in products:
            discount_rate    = float(DiscountRate.objects.get(product=product).rate)
            discounted_price = float(product.price) - (float(product.price) * discount_rate)
            
            is_in_wishlist   = 1 if WishList.objects.filter(user=user, product=product).exists() else 0

            # 오늘 기준 7일 이내 상품은 모두 신상품
            # 구매순 10위 안에 들면 베스트 상품
            product_dict = {
                            'product_id'       : product.id,
                            'product_name'     : product.name,
                            'product_price'    : float(product.price),
                            'product_thumbnail': product.thumbnail_image_url,
                            'discount_rate'    : discount_rate * 100,
                            'discounted_price' : discounted_price,
                            'stock'            : product.stock,
                            'is_in_wishlist'   : is_in_wishlist,
                            'is_new'           : 1 if product in Product.objects.filter\
                                                (updated_at__gte=datetime.datetime.today()-datetime.timedelta(days=7))\
                                                else 0,
                            'is_best'          : 1 if product in get_hot_products_querysets() else 0,
                            'is_sale'          : 1 if discount_rate > 0 else 0
                            }
            products_detail.append(product_dict)
        return products_detail
