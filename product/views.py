import json

from django.views import View
from django.http  import JsonResponse

from .models     import Category, SubCategory, Product, ProductImage, ProductDescription, BookDescription, DiscountRate, Option, ProductOption, Review, ProductInquiry
from user.models import User

class ProductShowInformationView(View):
    def get(self, request):
        productshowinformations = Product.objects.all()
        productimages           = Product.productimage.all()
        productdescriptions     = Product.productdescription.all()
        bookdescriptions        = Product.bookdescription.all()
        options                 = Product.product_options.filter(subcategory=data['subcategory'])
        discount_rates          = Product.discountrate.filter(product=data['product'])
        productoptions          = Product.product_options.filter(stock=data['stock'], additional_price=data['additional_price'])
        reviews                 = Product.review.all()
        product_inquiry         = Product.product_inquiry.all()

        result = []
        
        for productshowinformation in productshowinformations:
            productshowinformation_dict = {
                'name'               : productshowinformation.name,
                'price'              : productshowinformation.price,
                'thumbnail_image_url': productshowinformation.thumbnail_image_url
            }
        for productimage in productimages:
            productimage_dict = {
                'image_url' : image_url,
                'product' : productshowinformations
            }    
        for productdescription in productdescriptions:
            prductdescription_dict = {
                'name' : name,
                'material' : material,
                'size_cm' : size_cm,
                'manufacture_country' : manufacture_country,
                'caution' : caution,
                'product' : productshowinformations
            }
        for bookdescription in bookdescriptions:
            bookdescription_dict = {
                'title' : title,
                'publisher' : publisher,
                'size_mm' : size_mm,
                'total_page' : total_page,
                'product' : productshowinformations
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
                'rate' : discount_rate.rate
            }
        for review in reviews:
            review_dict = {
                'content' : review.content,
                'product' : review.productshowinformations,
                'user'    : review.user.user
                
            }
        result.append(productshowinformation_dict, option_dict, discount_rate_dict)
        return JsonResponse({'result' : result}, status=200)