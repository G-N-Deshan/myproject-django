from django.contrib import admin
from .models import Card, Cloths, Offers, NewArrivals, Review, ContactMessage, Toy, WishlistItem, Cart, CartItem, Order, OrderItem 


admin.site.register(Card)
admin.site.register(Offers)
admin.site.register(NewArrivals)
admin.site.register(Cloths)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['name', 'email']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['created_at', 'is_read']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    
    
@admin.register(Toy)
class ToyAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'age_range', 'price', 'is_bestseller', 'is_new']
    list_filter = ['category', 'age_range', 'is_bestseller', 'is_new']
    search_fields = ['name', 'description']
    
    
@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'item_type', 'get_item_name', 'added_at']
    list_filter = ['item_type', 'added_at', 'user']
    search_fields = ['user__username', 'cloth__name', 'toy__name']
    readonly_fields = ['added_at']
    
    def get_item_name(self, obj):
        return obj.get_item().name
    
    get_item_name.short_description = 'Item Name'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_item_count', 'get_total', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'session_key']
    
    def get_item_count(self, obj):
        return obj.get_item_count()
    
    def get_total(self, obj):
        return f"${obj.get_total():.2f}"
    
    get_item_count.short_description = 'Items'
    get_total.short_description = 'Total'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'item_type', 'get_item_name', 'quantity', 'get_subtotal']
    list_filter = ['item_type', 'added_at']
    
    def get_item_name(self, obj):
        item = obj.get_item()
        return item.name if hasattr(item, 'name') else item.title
    
    def get_subtotal(self, obj):
        return f"${obj.get_subtotal():.2f}"
    
    get_item_name.short_description = 'Item'
    get_subtotal.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'full_name', 'total', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'payment_method']
    search_fields = ['order_number', 'user__username', 'email', 'full_name']
    readonly_fields = ['order_number', 'created_at', 'updated_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'item_name', 'quantity', 'price', 'subtotal']
    list_filter = ['item_type']