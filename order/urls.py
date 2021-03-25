from django.urls import path
from .views      import ApplyCouponView

urlpatterns = [
    path('/coupon/<int:product_id>', ApplyCouponView.as_view())
          
]
