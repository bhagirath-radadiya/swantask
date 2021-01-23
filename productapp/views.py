from django.shortcuts import render, redirect
from django.db.models import Count, CharField, Value
from django.db import models
from django.db.models import Q
from regex import F
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import TrigramDistance
from .models import Product
from django.contrib import messages
from django.contrib.postgres.search import TrigramSimilarity


# Create your views here.

def index(request):
    render_dict = {}
    render_dict['max_quatity_product'] = Product.objects.all().order_by('-quantity')[
                                         0:20]  # products based on max. quantity
    render_dict['latest_product'] = Product.objects.all().order_by('-id')[0:20]  # last listed show first
    print(render_dict)

    return render(request, 'index.html', render_dict)


def viewProductDetail(request):
    render_dict = {}
    productId = request.GET['productId']

    get_product = Product.objects.get(pk=productId)
    render_dict['get_product'] = get_product

    similar_product = Product.objects.filter(category=get_product.category).exclude(
        pk=productId)  # remove current product from similer product
    render_dict['similar_product'] = similar_product

    return render(request, 'productDetail.html', render_dict)


def shop(request):
    render_dict = {}

    render_dict['brand'] = Product.objects.values('brand').annotate(brand_count=models.Count("brand"))
    render_dict['category'] = Product.objects.values('category').annotate(category_count=models.Count("category"))

    if request.method == 'GET':
        render_dict['product'] = Product.objects.filter(brand=render_dict['brand'][0]['brand'])
        print(render_dict['product'])

    if request.method == 'POST':
        product = Product.objects.all()
        if 'brand' in request.POST:
            brand = request.POST['brand']
            render_dict['brand_active'] = brand
            product = product.filter(brand=brand)
        if 'category' in request.POST:
            category = request.POST['category']
            render_dict['category_active'] = category
            product = product.filter(category=category)
        if 'search' in request.POST:
            search = request.POST['search']
            product = Product.objects.annotate(search=SearchVector('name', 'category', 'brand'), ).filter(search=search)
        render_dict['product'] = product

    return render(request, 'category.html', render_dict)


