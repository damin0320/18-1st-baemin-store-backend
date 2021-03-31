from django.urls import path
from .views      import (
                         LoginView, SignUpView, CouponRegistryView,
                         UserCouponView, WishListView, KakaoLoginView,
                         KakaoLoginCallbackView
                        )   


urlpatterns = [
    path('/login', LoginView.as_view()),
    path('/sign-up', SignUpView.as_view()),
    path('/coupon', CouponRegistryView.as_view()),
    path('/coupon/user', UserCouponView.as_view()),        
    path('/wishlist', WishListView.as_view()),
    path('/login/kakao', KakaoLoginView.as_view()),
    path('/login/kakao/oauth', KakaoLoginCallbackView.as_view()),
]
