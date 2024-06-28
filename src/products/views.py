from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django_htmx.http import HttpResponseLocation
from django.conf import settings
import spacy

from products.models import Product, ProductCategory
from products.forms import ProductForm

nlp = spacy.load("nl_core_news_sm")

wanted_UPOS_tags = ["NOUN", "PROPN", "VERB"]

def index(request):
    product_list = Product.objects.order_by("-updated_at")
    
    page_num = request.GET.get('page', 1)

    paginator = Paginator(product_list, 10) # number of items per page
    
    try:
        products_page = paginator.page(page_num)
    except PageNotAnInteger:
        products_page = paginator.page(1)
        print("PageNotAnInteger")
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
        print("Empty page")
    
    return render(
        request,
        "products/index.html",
        {
            "products_page": products_page,
            "use_photos": settings.USE_PHOTOS,
        }
    )

def product(request, product_id):
    new_product = False
    
    if request.method == "POST":
        if product_id == 0:
           form = ProductForm(request.POST)
        else:
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                raise Http404("Product does not exist")
            form = ProductForm(request.POST, instance=product)
            
        if form.is_valid():
            model = form.save(commit=False)
            
            doc = nlp(model.name + ". " + model.description)
            keywords = set()
            for token in doc:
                if token.pos_ in wanted_UPOS_tags:
                    keywords.add(token.text.lower())
            model.keywords = " ".join(keywords)

            model.save()
            
            redirect_value = request.POST.get("redirect-to")
            
            redirect_url = reverse("products:index")
            if redirect_value == "new":
                redirect_url = reverse("products:new")
            else:
                redirect_url = reverse("products:index")
            
            return HttpResponseLocation(redirect_url)
    
    else:
        if product_id == 0:
            form = ProductForm()
            new_product = True
        else:
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                raise Http404("Product does not exist")
            form = ProductForm(instance=product)
    
    return render(
            request,
            "products/product.html",
            {
                "form": form,
                "new_product": new_product,
                "use_photos": settings.USE_PHOTOS,
            }
        )