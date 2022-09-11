from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Brand
from typing import Optional
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)
from .forms import BrandForm
from django.utils import timezone

# Create your views here.


class BrandCreateView(CreateView):
    form_class = BrandForm
    template_name = "brand/brand_add.html"
    success_url: Optional[str] = reverse_lazy("backend:brand:brand_list")


class BrandListView(ListView):
    model = Brand
    queryset = Brand.objects.all().order_by("-created_at")
    context_object_name: Optional[str] = "brand_list"
    paginate_by: int = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = self.get_queryset().count()  # type: ignore
        return context


class BrandDetailView(DetailView):
    model = Brand
    queryset = Brand.objects.filter(is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context[""] =
        return context

    def get_object(self):
        obj = super().get_object()
        obj.last_access = timezone.now()
        obj.save(update_fields=["last_access"])
        return obj
