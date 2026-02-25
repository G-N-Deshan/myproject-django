from django.contrib import admin
from .models import Card, Cloths, Offers, NewArrivals


admin.site.register(Card)
admin.site.register(Offers)
admin.site.register(NewArrivals)
admin.site.register(Cloths)

# Register your models here.
