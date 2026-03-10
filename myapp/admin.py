
from django.contrib import admin
from .models import Card, Cloths, Offers, NewArrivals, Review, ContactMessage, Toy, WishlistItem, Cart, CartItem, Order, OrderItem, ProductReview


admin.site.register(Card)


@admin.register(Offers)
class OffersAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'offers_badge', 'price1', 'price2', 'end_time']
    list_filter = ['category']
    search_fields = ['title', 'description']
    ordering = ['-id']
    fieldsets = (
        ('Basic Info', {
            'fields': ('imageUrl', 'title', 'offers_badge', 'description', 'button_text', 'category'),
        }),
        ('Pricing', {
            'fields': ('price1', 'price2', 'stock_text', 'end_time'),
        }),
        ('Product Detail Page Content', {
            'fields': ('long_description', 'features', 'material'),
            'description': 'These fields appear on the product detail page. '
                           'For "Features", enter one feature per line.',
            'classes': ('collapse',),
        }),
    )


@admin.register(NewArrivals)
class NewArrivalsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'offers_badge', 'price']
    list_filter = ['category']
    search_fields = ['title', 'description']
    ordering = ['-id']
    fieldsets = (
        ('Basic Info', {
            'fields': ('imageUrl', 'title', 'offers_badge', 'description', 'price', 'category'),
        }),
        ('Product Detail Page Content', {
            'fields': ('long_description', 'features', 'material'),
            'description': 'These fields appear on the product detail page. '
                           'For "Features", enter one feature per line.',
            'classes': ('collapse',),
        }),
    )


@admin.register(Cloths)
class ClothsAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'subcategory', 'price1', 'discount_text']
    list_filter = ['category', 'subcategory']
    search_fields = ['name', 'desccription']
    ordering = ['-id']
    fieldsets = (
        ('Basic Info', {
            'fields': ('imageUrl', 'name', 'desccription', 'category', 'subcategory'),
        }),
        ('Pricing', {
            'fields': ('price', 'price1', 'price2', 'discount_text'),
        }),
        ('Product Detail Page Content', {
            'fields': ('long_description', 'features', 'material', 'care_instructions', 'sizes_available'),
            'description': 'These fields appear on the product detail page. '
                           'Enter "Features" one per line. '
                           'Enter "Sizes" comma-separated (e.g. S, M, L, XL).',
            'classes': ('collapse',),
        }),
    )

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
    fieldsets = (
        ('Basic Info', {
            'fields': ('imageUrl', 'name', 'description', 'category', 'age_range'),
        }),
        ('Pricing & Flags', {
            'fields': ('price', 'original_price', 'rating', 'is_bestseller', 'is_new'),
        }),
        ('Product Detail Page Content', {
            'fields': ('long_description', 'features', 'material', 'safety_info', 'dimensions'),
            'description': 'These fields appear on the product detail page. '
                           'Enter "Features" one per line.',
            'classes': ('collapse',),
        }),
    )
    
    
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


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_type', 'rating', 'title', 'created_at']
    list_filter = ['product_type', 'rating', 'created_at']
    search_fields = ['name', 'title', 'comment']
    readonly_fields = ['created_at']

