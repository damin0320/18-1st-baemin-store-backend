from django.urls import path
from .views      import CartView, SelectCartView

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('/payment', SelectCartView.as_view()),
]
