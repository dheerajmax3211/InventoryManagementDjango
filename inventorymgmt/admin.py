from django.contrib import admin
from .forms import InventoryCreateForm

# Register your models here.

from .models import Category, Inventory


class InventoryCreateAdmin(admin.ModelAdmin):
   list_display = ['category', 'item_name', 'quantity']
   form = InventoryCreateForm
   list_filter = ['category']
   search_fields = ['category', 'item_name']



admin.site.register(Inventory, InventoryCreateAdmin)
admin.site.register(Category)