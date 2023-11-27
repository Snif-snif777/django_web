from django.contrib import admin
from django.utils.html import format_html
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', 'display_image', 'description')
    search_fields = ('category_name', 'slug')
    prepopulated_fields = {'slug': ('category_name',)}
    list_per_page = 20

    def display_image(self, obj):
        if obj.cat_image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.cat_image.url))
        return 'No Image'
    display_image.short_description = 'Category Image'

admin.site.register(Category, CategoryAdmin)
