# Remove unused import
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItem
from store.models import Product, Variation
from decimal import Decimal


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    if request.method == 'POST':
        product_variation = []
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(
                    variation_category__iexact=key,
                    variation_value__iexact=value,
                    product__id=product_id
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart
        ).exists()

        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product, cart=cart)

            ex_ver_list = []
            id_list = []
            for item in cart_items:
                existing_variation = item.variations.all()
                ex_ver_list.append(list(existing_variation))
                id_list.append(item.id)

            print(ex_ver_list)

            if product_variation in ex_ver_list:
                index = ex_ver_list.index(product_variation)
                item_id = id_list[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(
                    product=product, quantity=1, cart=cart
                )
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()

        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id
        )
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        # Handle or log the exception if needed
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.filter(
        product=product, cart=cart, id=cart_item_id)
    cart_item.delete()

    return redirect('cart')


def cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        total = Decimal(0)
        quantity = 0

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        cart_items = []
        total = quantity = tax = grand_total = 0

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)
