from django.urls import path
from .views      import ProductView

urlpatterns = [
    path('/registry', ProductView.as_view()),
]
