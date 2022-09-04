from django.db import models
from core.models import BaseModel
from smartfields import fields
from smartfields.dependencies import Dependency
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from versatileimagefield.fields import VersatileImageField, PPOIField
import os
import uuid
from django.urls import reverse
from .managers import CategoryManager

# Create your models here.


def get_category_name(value, instance, **kwargs):
    return instance.category_name


def rename_path_and_save_category(path):
    def wrapper(instance, filename):
        ext = filename.split(".")
        if instance.id:
            category_id = "cid_%s" % (instance.category.id)
            category_name = "%s" % (instance.category_name)
            filename = "{}_{}_{}.{}".format(
                category_id, category_name, uuid.uuid4().hex, ext
            )
        else:
            random_id = "r_id%s" % (uuid.uuid4().hex)
            filename = "{}_{}".format(random_id, filename)
        return os.path.join(path, filename)

    return wrapper


category_image_upload_path = rename_path_and_save_category("category_images/")
# assign it `__qualname__`
category_image_upload_path.__qualname__ = "category_image_upload_path"


class Category(BaseModel):
    category_name = models.CharField(max_length=255)
    slug = fields.SlugField(
        dependencies=[Dependency(default=get_category_name, processor=slugify)],
        unique=True,
    )
    description = RichTextField()
    category_url = models.URLField(max_length=255)
    category_image = VersatileImageField(
        "Category Image", upload_to=category_image_upload_path, ppoi_field="image_ppoi"
    )
    image_ppoi = PPOIField()

    object = CategoryManager()

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("category_update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("category_delete", kwargs={"slug": self.slug})

    def deactivate(self):
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    # def save(self, *args, **kwargs):
    #     super(Category, self).save(*args, **kwargs)
    #     self.slug = slugify("{}-{}".format(self.category_name, self.id))
    #     super(Category, self).save(*args, **kwargs)
