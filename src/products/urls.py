from django.urls import path
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy

from . import views

app_name = "products"
urlpatterns = [
    # ex: /products/
    path("", views.index, name="index"),
    # redirect /products/0/ to /products/new/
    path("0/", RedirectView.as_view(url=reverse_lazy("products:new"))),
    # ex: /products/5/
    path("<int:product_id>/", views.product, name="update"),
    # ex: /products/new/
    path("new/", views.product, kwargs={"product_id": 0}, name="new"),
]