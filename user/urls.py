from django.urls import path
from .views      import LoginView, SignUpView, CouponRegistryView, UserCouponView

urlpatterns = [
    path('/login', LoginView.as_view()),
    path('/sign-up', SignUpView.as_view()),
    path('/couponregistry', CouponRegistryView.as_view()),
    path('/usercoupon', UserCouponView.as_view())        
]
