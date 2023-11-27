from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name',
                    'is_active', 'is_admin', 'is_staff', 'is_superadmin', 'last_login', 'date_joined')
    list_display_links = ('email', 'username')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_admin', 'is_staff', 'is_superadmin')
    ordering = ('email', '-date_joined',)
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {
         'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active',
         'is_admin', 'is_staff', 'is_superadmin')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2'),
        }),
    )

    filter_horizontal = ()

    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected users as active"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Mark selected users as inactive"


# Register the Account model with the custom admin class
admin.site.register(Account, AccountAdmin)
