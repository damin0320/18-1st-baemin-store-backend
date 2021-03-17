from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100, unique=True)
    email    = models.EmailField(max_length=128, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5)
    detailed_address = models.CharField(max_length=30)
    point = models.DecimalField(max_digits=10, decimal_places=2)


class UserCoupon(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    coupon = models.ForeignKey('Coupon', on_delete=models.CASCADE)


class Coupon(models.Model):
    name = models.CharField(max_length=20, unique=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField()


class Address(models.Model):
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5)
    detailed_address = models.CharField(max_length=30)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
