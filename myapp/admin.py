from django.contrib import admin
from .models import Card, Cloths, Offers, NewArrivals, Review   


admin.site.register(Card)
admin.site.register(Offers)
admin.site.register(NewArrivals)
admin.site.register(Cloths)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['name', 'email']

# Register your models here.
