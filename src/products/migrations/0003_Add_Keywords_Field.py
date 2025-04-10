# Generated by Django 5.0.6 on 2024-06-13 12:22

import django.contrib.postgres.indexes
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_Add_Extensions'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='keywords',
            field=models.TextField(blank=True, verbose_name='Zoekwoorden'),
        ),
        migrations.AlterField(
            model_name='product',
            name='amount',
            field=models.IntegerField(verbose_name='Aantal'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.productcategory', verbose_name='Categorie'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, verbose_name='Omschrijving'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Naam'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Naam'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=django.contrib.postgres.indexes.GinIndex(fields=['keywords'], name='product_keywords_gin_idx', opclasses=['gin_trgm_ops']),
        ),
    ]
