from django.urls import path, include
from category import urls as category_urls
from brand import urls as brand_urls

app_name = "backend"

urlpatterns = [
    path("category/", include(category_urls, namespace="category")),
    path("brand/", include(brand_urls, namespace="brand")),
]
