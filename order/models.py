from django.db import models


class OrderStatus(models.Model):
    status = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = 'order_status'


class Order(models.Model): 
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
    delivery_address = models.CharField(max_length=100, null=True)
    postal_code      = models.CharField(max_length=5, null=True)
    detailed_address = models.CharField(max_length=30, null=True)
    receiver_name    = models.CharField(max_length=30, null=True)
    phone_number     = models.CharField(max_length=11, null=True)
    customor_message = models.CharField(max_length=200, null=True)
    user             = models.ForeignKey('user.User', on_delete=models.CASCADE)
    order_status     = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'


class Cart(models.Model): 
    quantity       = models.IntegerField(default=1)
    user           = models.ForeignKey('user.User', on_delete=models.CASCADE)    
    product        = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    order          = models.ForeignKey('Order', on_delete=models.CASCADE)
    product_option = models.ForeignKey('product.ProductOption', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'carts'
        unique_together = ('user', 'product', 'order', 'product_option')


class WishList(models.Model):
    quantity       = models.IntegerField(default=1)
    product        = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    user           = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product_option = models.ForeignKey('product.ProductOption', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'wishlist'
        unique_together = ('product', 'user', 'product_option')
