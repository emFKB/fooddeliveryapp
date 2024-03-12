from django.contrib import admin
from .models import Item, Restaurant

admin.site.register(Restaurant)
admin.site.register(Item)