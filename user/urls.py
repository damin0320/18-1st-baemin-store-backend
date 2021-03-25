from django.urls import path
from .views      import LoginView, SignUpView, WishListView

urlpatterns = [
    path('/login', LoginView.as_view()),
    path('/sign-up', SignUpView.as_view()),
    path('/wishlist', WishListView.as_view()),
]
