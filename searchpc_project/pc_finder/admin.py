from django.contrib import admin
from .models import SearchLog

@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'purpose', 'budget', 'location')
    list_filter = ('purpose', 'timestamp')
    search_fields = ('purpose', 'location')
