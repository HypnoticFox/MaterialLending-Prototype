from django.db import models
from django.urls import reverse
from django.contrib.postgres.indexes import GinIndex
from django.core.validators import MinValueValidator, MaxValueValidator
from unidecode import unidecode

class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Naam")
    order = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(999)], verbose_name="Volgorde")

    def __str__(self):
        return self.name
    
    def clean(self):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                setattr(self, field.name, unidecode(getattr(self, field.name)).strip())
        
        self.name = self.name.title()
    
    class Meta:
        verbose_name = "ProductCategorie"
        verbose_name_plural = "ProductCategorieën"
    
class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Naam")
    description = models.TextField(blank=True, verbose_name="Omschrijving")
    amount = models.IntegerField(verbose_name="Aantal", validators=[MinValueValidator(1)])
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, verbose_name="Categorie")
    keywords = models.TextField(blank=True, verbose_name="Zoekwoorden")
    image_public_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def get_absolute_url(self):
        return reverse('products:update', kwargs={"product_id": str(self.id)})

    def __str__(self):
        return self.name
    
    def clean(self):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                setattr(self, field.name, unidecode(getattr(self, field.name)).strip())
        
        self.name = self.name.title()
        self.description = self.description.capitalize()
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Producten"
        indexes = [
            GinIndex(name='product_keywords_gin_idx', fields=['keywords'], opclasses=['gin_trgm_ops'])
        ]