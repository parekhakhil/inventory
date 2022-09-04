from django.urls import path, include
from category.api import urls as category_api

app_name = "api"

urlpatterns = [
    path("category/", include(category_api, namespace="category_api")),
]
