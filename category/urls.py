from django.urls import path, include
from . import views

app_name = "category"

urlpatterns = [
    path('all/',views.CategoryListView.as_view(),name='category_list'),
    path('add/',views.CategoryCreateView.as_view(),name='category_add'),
    path('<str:slug>/',views.CategoryDetailView.as_view(),name='category_detail'),
]
