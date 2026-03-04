from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name = 'contact'),
   
    path('buy/', views.buy, name= 'buy'),
    path('shop-offers/', views.shop_offers, name= 'shop_offers'),
    path('new_arrivals/', views.new_arrivals, name= 'new_arrivals'),
    path('login/', views.login, name = 'login'),
    path('signup/', views.signup, name = 'signup'), 
    path('product/<str:product_type>/<int:product_id>/', views.product_detail, name='product_detail'), 
    path('cloths/', views.cloths, name='cloths'),
    path('toys/', views.toys, name='toys'),
    path('kids_cloths/', views.kids_cloths, name='kids_cloths'),
    path('women_cloths/', views.women_cloths, name='women_cloths'),
    path('mens_cloths/', views.mens_cloths, name='mens_cloths'),
    path('reviews/', views.reviews, name='reviews'),
    path('review-success/', views.review_success, name='review_success'),
    path('contact/', views.contact_us, name='contact_us'),
    path('contact-success/', views.contact_success, name='contact_success'),
    path('toys/', views.toys_page, name='toys_page'),
    path('cart/', views.cart, name='cart'),
    path('cart_details_page/', views.cart_details, name='cart_details'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    