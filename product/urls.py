from django.urls      import path
from django.conf.urls import re_path
from .views           import CategoryView

urlpatterns = [
    re_path(r'^/category/(?P<category_name>[ㄱ-ㅎ가-힣]+)$', CategoryView.as_view()),
]
