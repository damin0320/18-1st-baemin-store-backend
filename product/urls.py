from django.urls      import path
from .views           import CategoryView

urlpatterns = [
    path(r'/category/<str:category_name>', CategoryView.as_view()),
]
