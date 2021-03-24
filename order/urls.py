from django.urls import path
from .views      import CartView, SelectCartView, OrderView

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('/payment', SelectCartView.as_view()),
    path('', OrderView.as_view()),
]
