from django.urls import path, include
from category.api import urls as category_api
from brand.api import urls as brand_api

app_name = "api"

urlpatterns = [
    path("category/", include(category_api, namespace="category_api")),
    path("brand/", include(brand_api, namespace="brand_api")),
]
