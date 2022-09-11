from django.db import models
from django.db.models.functions import Coalesce

class BrandManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def with_counts(self):
        return self.annotate(num_responses=Coalesce(models.Count("response"), 0))

    def active(self):
        return (
            super(BrandManager, self)
            .get_queryset()
            .filter(is_deleted=False)
            .order_by("created_at")
        )
