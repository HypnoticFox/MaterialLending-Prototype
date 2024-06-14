from django.db import models
from django.urls import reverse
from django.contrib.postgres.indexes import GinIndex

class ProductCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Naam")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "ProductCategorie"
        verbose_name_plural = "ProductCategorieën"
    
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Naam")
    description = models.TextField(blank=True, verbose_name="Omschrijving")
    amount = models.IntegerField(verbose_name="Aantal")
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, verbose_name="Categorie")
    keywords = models.TextField(blank=True, verbose_name="Zoekwoorden")
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={"product_id": str(self.id)})

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Producten"
        indexes = [
            GinIndex(name='product_keywords_gin_idx', fields=['keywords'], opclasses=['gin_trgm_ops'])
        ]