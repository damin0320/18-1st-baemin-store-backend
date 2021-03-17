from django.db import models


class OrderStatus(models.Model):
    status = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = 'order_status'


class Order(models.Model):
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True, null=True)
    user         = models.ForeignKey('user.User', on_delete=models.CASCADE)
    order_status = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'


class Cart(models.Model):
    quantity = models.IntegerField(default=1)
    product  = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    order    = models.ForeignKey('Order', on_delete=models.CASCADE)

    class Meta:
        db_table = 'carts'
        unique_together = ('product', 'order')


class WishList(models.Model):
    quantity = models.IntegerField(default=1)
    product  = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    user     = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishlist'
        unique_together = ('product', 'user')
