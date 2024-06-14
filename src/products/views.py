from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django_htmx.http import HttpResponse, HttpResponseLocation

from products.models import Product, ProductCategory

def index(request):
    product_list = Product.objects.all()
    
    page_num = request.GET.get('page', 1)

    paginator = Paginator(product_list, 1) # number of items per page
    
    try:
        products_page = paginator.page(page_num)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    
    base_template = "base_partial.html" if request.htmx else "base_complete.html"
    return render(
        request,
        "products/index.html",
        {
            "base_template": base_template,
            "products_page": products_page
        }
    )

def details(request, product_id):
    return HttpResponse(product_id)