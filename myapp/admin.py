from django.contrib import admin
from .models import Card, Cloths, Offers, NewArrivals, Review, ContactMessage, Toy  


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