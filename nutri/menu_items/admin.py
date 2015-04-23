from django.contrib import admin
from menu_items.models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'rest')
    search_fields = ('name', 'rest', 'valid')
    list_filter = ('name',)


admin.site.register(Item, ItemAdmin)