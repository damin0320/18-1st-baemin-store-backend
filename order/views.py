from django.views import View


PRODUCT_OPTION_ID = 1

PRODUCT_ID = 5


class CartView(View):
    def post(self, request):
        product_id        = PRODUCT_ID
        product_option_id = PRODUCT_OPTION_ID
        
        
