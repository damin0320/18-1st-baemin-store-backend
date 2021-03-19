from django.urls import path
from .views      import ProductShowInformationView

urlpatterns = [
    path('/product',ProductShowInformationView.as_view()),
]