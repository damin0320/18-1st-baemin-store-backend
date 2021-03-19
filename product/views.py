import json
from json import JSONDecodeError

from django.views import View
from django.http  import JsonResponse

from .models import Product

class ProductView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        category              = data['category']
        sub_category          = data['sub_category']
        name                  = data['name']
        price                 = data['price']
        thumbnail             = data['thumbnail']
        images                = data['images']
        stock                 = data['stock']
        discount_rate         = data.get('discount_rate', 0)
        option_classification = data.get('option_classification', None)
        
        if option_classification:
            options      = data['options']
            options_list = list()
            for option in options:
                _option = {
                    'option_name'     : option['option_name']
                    'additional_price': option['additional_price']
                    'option_stock'    : option['option_stock']
                }
                options_list.append(_option)
        
        if sub_category == 'book':
            title      = data['title']
            publisher  = data['publisher']
            total_page = data['total_page']
            size_mm    = data.get('size_mm', None)
        else:    
            material            = data.get('material', None)
            size_cm             = data.get('size_cm', None)
            manufacture_country = data.get('manufacture_country', None)
            caution             = data.get('caution', None)
        
        