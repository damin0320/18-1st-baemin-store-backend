from django.urls import path
from .views      import ProductView, ProductRegistryView

urlpatterns = [
    path('/<int:product_id>', ProductView.as_view()),
    path('', ProductRegistryView.as_view()),
]
