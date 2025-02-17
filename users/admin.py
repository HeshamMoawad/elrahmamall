from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ElRahmaUser
from django.contrib.admin import AdminSite

class ElRahmaUserAdmin(UserAdmin):
    model = ElRahmaUser
    list_display = ('email', 'phone_number', 'is_staff', 'is_active')
    list_filter = ( 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone_number', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'phone_number')
    ordering = ('email',)


admin.site.site_title = "ElRahmaMall Admin"
admin.site.site_header = "ElRahmaMall Admin"
admin.site.index_title = "ElRahmaMall Site"

admin.site.register(ElRahmaUser, ElRahmaUserAdmin)
