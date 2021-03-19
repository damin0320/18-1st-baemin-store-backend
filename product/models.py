from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'categories'


class SubCategory(models.Model):
    name     = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'


class CouponSubCategory(models.Model):
    coupon       = models.ForeignKey('user.Coupon', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'coupons_sub_categories'


class Product(models.Model):
    name                = models.CharField(max_length=30, unique=True)
    price               = models.DecimalField(max_digits=10, decimal_places=2)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    thumbnail_image_url = models.CharField(max_length=2000)
    sub_category        = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    recommendations     = models.ManyToManyField('self', symmetrical=True)
    product_options     = models.ManyToManyField('Option', through='ProductOption')

    class Meta:
        db_table = 'products'


class ProductImage(models.Model):
    image_url = models.CharField(max_length=2000)
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_images'


class ProductDescription(models.Model):
    name                = models.CharField(max_length=30, unique=True)
    material            = models.CharField(max_length=20, null=True)
    size_cm             = models.CharField(max_length=30, null=True)
    manufacture_country = models.CharField(max_length=30, null=True)
    caution             = models.CharField(max_length=200, null=True)
    product             = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_descriptions'


class BookDescription(models.Model):
    title      = models.CharField(max_length=30, unique=True)
    publisher  = models.CharField(max_length=30)
    size_mm    = models.CharField(max_length=30, null=True)
    total_page = models.IntegerField()
    product    = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'book_descriptions'


class Review(models.Model):
    content = models.CharField(max_length=500, null=True)
    rating  = models.SmallIntegerField(null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)
    order   = models.ForeignKey('order.Order', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'


class ProductInquiry(models.Model):
    content = models.CharField(max_length=500)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_inquiries'


class DiscountRate(models.Model):
    rate    = models.DecimalField(max_digits=3, decimal_places=2)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'discount_rates'
        unique_together = ('product', 'rate')
    

class Option(models.Model):
    classification = models.CharField(max_length=45)
    name           = models.CharField(max_length=45)

    class Meta:
        db_table        = 'options'
        unique_together = ('classification', 'name')

class ProductOption(models.Model):
    stock            = models.IntegerField()
    additional_price = models.DecimalField(max_digits=10, decimal_places=2)
    product          = models.ForeignKey('Product', on_delete=models.CASCADE)
    option           = models.ForeignKey('Option', on_delete=models.CASCADE)
    sub_category     = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_options'
