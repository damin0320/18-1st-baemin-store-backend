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
            options_list = dict()
            for option in options:
                options_list = {
                }

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
        