from django.urls import path
from .views      import CartView, OrderView

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('', OrderView.as_view()),
]
