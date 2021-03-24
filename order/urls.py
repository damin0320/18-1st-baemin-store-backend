from django.urls import path
from .views      import ApplyCouponView

urlpatterns = [
    path('/applycoupon', ApplyCouponView.as_view())
          
]
