from django import forms
from .models import Brand


class BrandForm(forms.ModelForm):

    class Meta:
        model = Brand
        fields = ['brand_name','description','brand_url','brand_image']
