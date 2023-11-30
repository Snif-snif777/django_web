from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')
    search_fields = ('cart_id',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'display_variations', 'cart',
                    'quantity', 'is_active', 'sub_total', 'get_date_added')
    list_editable = ('is_active',)
    # Change 'cart__date_added' to a valid field in Cart model
    list_filter = ('is_active', 'cart__date_added')
    search_fields = ('product__product_name', 'cart__cart_id', 'quantity')

    def display_variations(self, obj):
        return ", ".join([str(variation) for variation in obj.variations.all()])

    display_variations.short_description = 'Variations'

    def get_date_added(self, obj):
        return obj.cart.date_added

    get_date_added.short_description = 'Date Added'
