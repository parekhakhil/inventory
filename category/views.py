from django.urls import reverse_lazy
from django.utils import timezone
from typing import Optional
from django.shortcuts import render

from category.forms import CategoryForm
from .models import Category
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

# Create your views here.


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all().order_by("-created_at")
    context_object_name: Optional[str] = "category_list"
    paginate_by: int = 20

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context["total"] = self.get_queryset().count()  # type: ignore
        return context


class CategoryDetailView(DetailView):
    model = Category
    queryset = Category.objects.filter(is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context[""] =
        return context

    def get_object(self):
        obj = super().get_object()
        obj.last_access = timezone.now()
        obj.save(update_fields=["last_access"])
        return obj


class CategoryCreateView(CreateView):
    form_class = CategoryForm
    template_name: str = "category/category_add.html"
    success_url: Optional[str] = reverse_lazy("backend:category:category_list")
