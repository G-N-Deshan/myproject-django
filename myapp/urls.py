from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name = 'contact'),
    path('reviews/', views.reviews, name= 'reviews'),
    path('buy/', views.buy, name= 'buy'),
    path('shop-offers/', views.shop_offers, name= 'shop_offers'),
    path('new_arrivals/', views.new_arrivals, name= 'new_arrivals')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)