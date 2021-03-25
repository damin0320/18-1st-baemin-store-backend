from django.db.models import Sum

from order.models   import Cart
from product.models import Product


BEFORE_PURCHASE = 1
PENDING_PURCHASE = 2
PURCHASE_DONE = 3


def get_hot_products_querysets():
    """
    베스트상품 10개 가져오는 함수
    """
    cart_querysets = Cart.objects.filter(order__order_status=PURCHASE_DONE)

    hot_products = cart_querysets.values('product_id').\
                    annotate(total_quantity_sold=Sum('quantity'))\
                    .order_by('-quantity')[:10]

    product_querysets = Product.objects.none()
    for hot_product in hot_products:
        product_querysets |= Product.objects.filter(id=hot_product['product_id'])

    return product_querysets
