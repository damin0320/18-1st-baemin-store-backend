from django.urls import path
from django.conf.urls import re_path
from .views      import ProductView

urlpatterns = [
    re_path(r'^/(?P<product_id>\d+)$', ProductView.as_view()),
]
