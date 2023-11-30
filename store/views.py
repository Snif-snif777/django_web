from django.http import Http404
from django.shortcuts import get_object_or_404, render
from carts.models import CartItem
from .models import Product
from category.models import Category
from carts.views import _cart_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count


def store(request, category_slug=None):
    # Initial query for all products
    products = Product.objects.filter(is_available=True)

    # Filter by category if provided
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=categories)

    # Get the total count before pagination using annotate
    products = products.annotate(total_count=Count('id'))
    total_count = products.aggregate(total_count=Count('id'))['total_count']

    # Number of products per page
    products_per_page = 3

    # Explicitly order the queryset by id (you can choose a different field if needed)
    products = products.order_by('-created_date', 'id')
    # Pagination
    # Show products_per_page products per page
    paginator = Paginator(products, products_per_page)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Product count
    product_count = len(products)

    context = {
        'products': products,
        'product_count': product_count,
        'total_count': total_count,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        color_variations = single_product.variation_set.filter(
            variation_category='color').order_by('variation_value')
        size_variations = single_product.variation_set.filter(
            variation_category='size').order_by('variation_value')

        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(
            request), product=single_product).exists()

    except Product.DoesNotExist:
        raise Http404("Product not found")

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'color_variations': color_variations,
        'size_variations':  size_variations,
    }

    return render(request, 'store/product_detail.html', context)


def search_results(request):
    # Initialize products and product_count outside the if statement
    products = []
    product_count = 0
    total_count = 0

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        # Check if keyword is provided
        if keyword:
            products = Product.objects.order_by(
                '-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = len(products)
            total_count = products.aggregate(
                total_count=Count('id'))['total_count']

    context = {
        'products': products,
        'product_count': product_count,
        'total_count': total_count,

    }
    return render(request, 'store/store.html', context)
