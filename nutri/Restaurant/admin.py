from django.contrib import admin

from Restaurant.models import Restaurant


class RestAdmin(admin.ModelAdmin):
    list_display = ('name', 'cuisine1', 'user')
    search_fields = ('name', 'user', 'city', 'zipcode')
    list_filter = ('name',)


admin.site.register(Restaurant, RestAdmin)

# Register your models here.
