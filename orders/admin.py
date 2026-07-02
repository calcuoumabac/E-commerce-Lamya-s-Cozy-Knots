from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product_name', 'variant_details', 'quantity', 'price')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'wilaya', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'wilaya')
    search_fields = ('full_name', 'phone')
    list_editable = ('status',)
    inlines = [OrderItemInline]