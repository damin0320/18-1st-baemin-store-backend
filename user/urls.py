from django.urls import path
from .views      import LoginView, SignUpView, CouponView

urlpatterns = [
    path('/login', LoginView.as_view()),
    path('/sign-up', SignUpView.as_view()),
    path('/coupon', CouponView.as_view()),
    
]
