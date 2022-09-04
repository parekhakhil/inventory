from django.urls import path
from . import views

app_name = "category_api"

urlpatterns = [
    path("add/", views.CategoryCreateView.as_view(), name="category_create_api"),
    path("all/", views.ListCategoryView.as_view(), name="categroy_list_api"),
    path("<str:slug>/", views.CategoryDetailView.as_view(), name="category_detail_api"),
]
