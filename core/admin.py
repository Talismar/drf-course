from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(PublishingCompany)
admin.site.register(Author)
admin.site.register(Book)

class ItemsInline(admin.TabularInline):
    model = ItemsPurchase

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    inlines = (ItemsInline,)