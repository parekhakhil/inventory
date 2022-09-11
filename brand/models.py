from django.db import models
from brand.managers import BrandManager
from core.models import BaseModel
from smartfields import fields
from smartfields.dependencies import Dependency
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from versatileimagefield.fields import VersatileImageField, PPOIField
import os
import uuid

# Create your models here.


def get_brand_name(value, instance, **kwargs):
    return instance.brand_name


def rename_path_and_save_brand(path):
    def wrapper(instance, filename):
        ext = filename.split(".")
        if instance.id:
            brand_id = "bid_%s" % (instance.brand.id)
            brand_name = "%s" % (instance.brand_name)
            filename = "{}_{}_{}.{}".format(brand_id, brand_name, uuid.uuid4().hex, ext)
        else:
            random_id = "r_id%s" % (uuid.uuid4().hex)
            filename = "{}_{}".format(random_id, filename)
        return os.path.join(path, filename)

    return wrapper


brand_image_upload_path = rename_path_and_save_brand("brand_images/")
# assign it `__qualname__`
brand_image_upload_path.__qualname__ = "brand_image_upload_path"


class Brand(BaseModel):
    brand_name = models.CharField(
        max_length=128,
    )
    slug = fields.SlugField(
        dependencies=[Dependency(default=get_brand_name, processor=slugify)],
        unique=True,
    )
    description = RichTextField()
    brand_url = models.URLField(max_length=255, null=True, blank=True)
    brand_image = VersatileImageField(
        "Brand Image", upload_to=brand_image_upload_path, ppoi_field="image_ppoi"
    )
    image_ppoi = PPOIField()

    objects = BrandManager()

    def __str__(self):
        return self.brand_name

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
