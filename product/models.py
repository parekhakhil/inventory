from versatileimagefield.fields import VersatileImageField, PPOIField
import os
import uuid
from django.db import models
from core.models import BaseModel
from django.utils.text import slugify
from smartfields import fields
from smartfields.dependencies import Dependency
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from category.models import Category
from brand.models import Brand


def get_product_name(value, instance, **kwargs):
    return "{}-{}".format(instance.product_name, str(instance.category.id))


def rename_path_and_save_product(path):
    def wrapper(instance, filename):
        ext = filename.split(".")
        if instance.product.id:
            product_id = "pid_%s" % (instance.product.id)
            product_name = "%s" % (instance.product.product_name)
            filename = "{}_{}_{}.{}".format(
                product_id, product_name, uuid.uuid4().hex, ext
            )
        else:
            random_id = "r_id%s" % (uuid.uuid4().hex)
            filename = "{}_{}".format(random_id, filename)
        return os.path.join(path, filename)

    return wrapper


product_image_upload_path = rename_path_and_save_product("product_images/")
# assign it `__qualname__`
product_image_upload_path.__qualname__ = "product_image_upload_path"


class Product(BaseModel):
    product_name = models.CharField(max_length=255)
    slug = fields.SlugField(
        dependencies=[Dependency(default=get_product_name, processor=slugify)],
        unique=True,
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    product_detail = RichTextField()
    product_url = models.URLField(max_length=255)
    product_mrp = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product_name

    def get_saving(self):
        return int(self.product_mrp - self.selling_price)

    def get_saving_percent(self):
        saving = int(self.product_mrp - self.selling_price)
        return round((saving * 100) / self.product_mrp, 2)

    # def save(self, *args, **kwargs):
    #     super(Product, self).save(*args, **kwargs)
    #     self.slug = slugify("{}-{}".format(self.product_name, self.id))
    #     super(Product, self).save(*args, **kwargs)


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image_name = models.CharField(max_length=255)
    product_image = VersatileImageField(
        "Image",
        upload_to=product_image_upload_path,
        ppoi_field="image_ppoi",
        width_field="width",
        height_field="height",
    )
    image_ppoi = PPOIField()
    height = models.PositiveIntegerField("Image Height", blank=True, null=True)
    width = models.PositiveIntegerField("Image Width", blank=True, null=True)

    def __str__(self):
        return self.image_name
