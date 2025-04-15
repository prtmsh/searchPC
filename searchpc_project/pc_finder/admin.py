from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SearchLog, CustomUser

@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'purpose', 'budget', 'location')
    list_filter = ('purpose', 'timestamp')
    search_fields = ('purpose', 'location')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
