from django.db import models


class User(models.Model):
    username         = models.CharField(max_length=30, unique=True)
    password         = models.CharField(max_length=100, unique=True)
    email            = models.EmailField(max_length=128, unique=True)
    phone_number     = models.CharField(max_length=11, unique=True)
    address          = models.CharField(max_length=100)
    postal_code      = models.CharField(max_length=5)
    detailed_address = models.CharField(max_length=30, null=True)
    point            = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user_coupon      = models.ManyToManyField('Coupon', through='UserCoupon')

    class Meta:
        db_table = 'users'


class UserCoupon(models.Model):
    user     = models.ForeignKey('User', on_delete=models.CASCADE)
    coupon   = models.ForeignKey('Coupon', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table        = 'user_coupons'
        unique_together = ('user', 'coupon')


class Coupon(models.Model):
    name           = models.CharField(max_length=20, unique=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date     = models.DateTimeField(auto_now_add=True)
    expire_date    = models.DateTimeField()
    coupon_sub_category = models.ManyToManyField('product.SubCategory', through='product.CouponSubCategory')

    class Meta:
        db_table = 'coupons'


class DeliveryAddress(models.Model):
    address          = models.CharField(max_length=100)
    postal_code      = models.CharField(max_length=5)
    detailed_address = models.CharField(max_length=30, null=True)
    user             = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'delivery_addresses'
        unique_together = ('user', 'address', 'postal_code', 'detailed_address')
