from rest_framework import status, filters
from brand.models import Brand
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.response import Response
from .serializers import BrandSerializer
from core.views import CustomPagination
from django.utils import timezone


class BrandCreateView(GenericAPIView):
    """
    View for create category
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def post(self, request, *args, **kwargs):
        if not request.POST._mutable:
            request.POST._mutable = True
        data = request.data
        if data:
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "data": {"brand": serializer.data},
                        "message": "Category generated successfully",
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        "success": False,
                        "error": serializer.errors,
                        "message": "Something went wrong",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {
                    "success": False,
                    "error": "Please enter valid data",
                    "message": "Please enter valid data",
                },
                status=status.HTTP_204_NO_CONTENT,
            )


class ListBrandView(GenericAPIView):
    """
    View for listing categories
    """

    queryset = Brand.objects.all().order_by("-created_at")
    serializer_class = BrandSerializer
    pagination_class = CustomPagination
    ordering_fields = ["created_at"]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # filter_backend = self.filter_queryset(queryset)
        # serializer = self.get_serializer(filter_backend, many=True)
        serializer = self.get_serializer(queryset, many=True)
        data = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(data)


class BrandDetailView(RetrieveUpdateDestroyAPIView):
    """
    For updating and viewing single category
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_url_kwarg = "slug"
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"success": True, "data": serializer.data, "message": "Categroy retrieved"},
            # status=status.HTTP_201_CREATED,
        )

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.last_access = timezone.now()
        instance.save(update_fields=["last_access", "is_deleted"])
        serializer = self.get_serializer(instance)
        return Response(
            {"success": True, "data": serializer.data},
            status=status.HTTP_204_NO_CONTENT,
        )
