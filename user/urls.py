from django.urls import path
from .views      import LoginView, SignUpView, CouponRegistryView, UserCouponView

urlpatterns = [
    path('/login', LoginView.as_view()),
    path('/sign-up', SignUpView.as_view()),
    path('/coupon', CouponRegistryView.as_view()),
    path('/coupon/user', UserCouponView.as_view())        
]
