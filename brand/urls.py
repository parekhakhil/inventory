from django import views
from django.urls import path, include
from . import views

app_name = "brand"

urlpatterns = [
    path("all/", views.BrandListView.as_view(), name="brand_all"),
    path("add/", views.BrandCreateView.as_view(), name="brand_add"),
    path("<str:slug>/", views.BrandDetailView.as_view(), name="brand_detail"),
]
