import json
from json import JSONDecodeError

from django.views import View
from django.http  import JsonResponse

from .models      import Category, SubCategory, Product, ProductImage, ProductDescription, BookDescription, DiscountRate, Option, ProductOption, Review, ProductInquiry
from user.models  import User
from order.models import Order


class ProductView(View):
    def get(self, request, product_id):
        try:            
            product = Product.objects.get(id=product_id)

            product_name      = product.name
            product_price     = product.price
            product_thumbnail = product.thumbnail_image_url
            product_stock     = product.stock

            discount_rate    = DiscountRate.objects.get(product=product).rate
            discounted_price = product_price * discount_rate
            
            discount_rate *= 100

            product_images = ProductImage.objects.filter(product=product)
            images_list = list()
            for product_image in product_images:
                image_url = product_image.image_url
                images_list.append(image_url)

            products_options = ProductOption.objects.filter(product=product)
            options_list = list()
            for product_option in products_options:
                option = Option.objects.get(id=product_option.option_id)

                option_dict = dict(
                                option_name             = option.name,
                                option_classification   = option.classification,
                                option_stock            = product_option.stock,
                                option_additional_price = product_option.additional_price,
                                product_option_id       = product_option.id
                                )
                options_list.append(option_dict)

            category_name = product.sub_category.category.name

            if category_name == '책':
                book_description = BookDescription.objects.get(product=product)

                detailed_description = dict(
                                            title      = book_description.title,
                                            publisher  = book_description.publisher,
                                            size_mm    = book_description.size_mm,
                                            total_page = book_description.total_page
                                        )
            else:
                product_description = ProductDescription.objects.get(product=product)

                detailed_description = dict(
                                            name                = product_description.name,
                                            material            = product_description.material,
                                            size_cm             = product_description.size_cm,
                                            manufacture_country = product_description.manufacture_country,
                                            caution             = product_description.caution
                                        )           

            product_inquiries = ProductInquiry.objects.filter(product=product)
            inquiries_list = list()
            for product_inquiry in product_inquiries:
                product_inquiry_content  = product_inquiry.content
                product_inquiry_username = product_inquiry.user.username
            
            # TODO: add review contents
            results = dict(
                        category_name        = category_name,
                        product_name         = product_name,
                        product_price        = product_price,
                        product_thumbnail    = product_thumbnail,
                        product_stock        = product_stock,
                        discount_rate        = discount_rate,
                        images_list          = images_list,
                        options_list         = options_list,
                        detailed_description = detailed_description,
                        inquiries_list       = inquiries_list,
                        reviews_list         = ''
                        )
            
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
