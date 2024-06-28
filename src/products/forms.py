from django.forms import ModelForm, HiddenInput, ModelChoiceField, CharField
from products.models import Product, ProductCategory

class ProductForm(ModelForm):
    
    category = ModelChoiceField(
        queryset=ProductCategory.objects.order_by("order", "name"),
        empty_label=None,
        label=Product._meta.get_field("category").verbose_name.title()
        )
    
    image_public_id = CharField(widget=HiddenInput(), required=False)
    
    class Meta:
        model = Product
        fields = ["name", "description", "amount", "category", "image_public_id"]