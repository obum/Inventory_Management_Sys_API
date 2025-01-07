from django.contrib import admin
from .models import ChangeReason, InventoryChange, InventoryItem, Category

# Register your models here.

admin.site.register(InventoryItem)
admin.site.register(ChangeReason)
admin.site.register(InventoryChange)
admin.site.register(Category)
