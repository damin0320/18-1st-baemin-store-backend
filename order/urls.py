from django.urls import path
from .views      import ApplyCouponView

urlpatterns = [
    path('/coupon/apply', ApplyCouponView.as_view())
          
]
