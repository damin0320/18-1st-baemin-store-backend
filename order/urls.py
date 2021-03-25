from django.urls import path
from .views      import CartView, OrderView, ApplyCouponView

urlpatterns = [
    path('/coupon/<int:product_id>', ApplyCouponView.as_view()),
    path('/cart', CartView.as_view()),
    path('', OrderView.as_view()),
    ]
