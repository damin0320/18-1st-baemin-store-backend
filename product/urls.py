from django.urls      import path
from .views           import CategoryView, ProductView, ProductRegistryView


urlpatterns = [
    path('/<int:product_id>', ProductView.as_view()),
    path(r'/category/<str:category_name>', CategoryView.as_view()),
    path('', ProductRegistryView.as_view()),
]
