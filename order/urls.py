from django.urls import path
from .views      import WishListView

urlpatterns = [
    path('/wishlist', WishListView.as_view()),
]

