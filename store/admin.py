from django.utils.html import format_html
from django.contrib import admin
from .models import Product, Variation


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'display_image',
                    'is_available', 'created_date', 'modified_date')
    list_filter = ('is_available', 'category')
    search_fields = ('product_name', 'description', 'category__category_name')
    prepopulated_fields = {'slug': ('product_name',)}
    date_hierarchy = 'created_date'
    ordering = ('-created_date',)

    def display_image(self, obj):
        if obj.images:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.images.url))
        return 'No Image'
    display_image.short_description = 'Product Image'


admin.site.register(Product, ProductAdmin)


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_date')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'is_active')
    search_fields = ('product__name', 'variation_value')
    readonly_fields = ('created_date',)
    raw_id_fields = ('product',)

    fieldsets = (
        ('General Information', {
            'fields': ('product',)
        }),
        ('Variation Details', {
            'fields': ('variation_category', 'variation_value', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_date',),
            'classes': ('collapse',)  # Hide this section by default
        }),
    )