from django.urls import path
from . import views

app_name = "brand_api"

urlpatterns = [
    path("all/", views.ListBrandView.as_view(), name="brand_list_api"),
    path("add/", views.BrandCreateView.as_view(), name="brand_add_api"),
    path("<str:slug>/", views.BrandDetailView.as_view(), name="brand_detail_api"),
]
