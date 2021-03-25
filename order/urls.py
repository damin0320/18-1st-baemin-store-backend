from django.urls import path
from .views      import ApplyCouponView

urlpatterns = [
    path('/apply-coupon', ApplyCouponView.as_view())
          
]
