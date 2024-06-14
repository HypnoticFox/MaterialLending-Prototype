from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    # ex: /products/
    path("", views.index, name="index"),
    # ex: /products/5/
    path("<int:product_id>/", views.details, name="details"),
]