import json

from django.views import View
from django.http  import JsonResponse

from .models      import Category, SubCategory, Product, ProductImage, ProductDescription, BookDescription, DiscountRate, Option, ProductOption, Review, ProductInquiry
from user.models  import User
from order.models import Order

class ProductShowInformationView(View):
    def get(self, request):
        products            = Product.objects.all()
        productimages       = Product.productimage.all()
        productdescriptions = Product.productdescription.all()
        bookdescriptions    = Product.bookdescription.all()
        options             = Product.product_options.filter(subcategory=data['subcategory'])
        discount_rates      = Product.discountrate.filter(product=data['product'])
        productoptions      = Product.product_options.filter(stock=data['stock'], additional_price=data['additional_price'])
        reviews             = Product.review.all()
        product_inquiry     = Product.product_inquiry.all()

        result = []
        
        for product in products:
            product_dict = {
                'name'               : product.name,
                'price'              : product.price,
                'thumbnail_image_url': product.thumbnail_image_url,
                'stock'              : stock,
                'sub_category'       : sub_category
            }
        for productimage in productimages:
            productimage_dict = {
                'image_url' : image_url,
                'product' : productshowinformations,
            }    
        for productdescription in productdescriptions:
            prductdescription_dict = {
                'name' : name,
                'material' : material,
                'size_cm' : size_cm,
                'manufacture_country' : manufacture_country,
                'caution' : caution,
                'product' : product
            }
        for bookdescription in bookdescriptions:
            bookdescription_dict = {
                'title' : title,
                'publisher' : publisher,
                'size_mm' : size_mm,
                'total_page' : total_page,
                'product' : product
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
                'product'         : product,
                'option'          : option,
                'sub_category'    : sub_category
            }
        for discount_rate in discount_rates:
            discount_rate_dict = {
                'rate'   : discount_rate.rate,
                'product': product
            }
        for review in reviews:
            review_dict = {
                'content': review.content,
                'product': review.productshowinformations,
                'user'   : review.user.user,
                'product': product,
                'order'  : order
            }
        for product_inquiry in product_inquiriesL:
            product_inquiry_dict = {
                'content': content,
                'product': product,
                'user'   : user
            }
        result.append(productshowinformation_dict, option_dict, discount_rate_dict)
        return JsonResponse({'result' : result}, status=200)