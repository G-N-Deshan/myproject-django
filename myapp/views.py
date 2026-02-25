from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from .models import Card, Offers, NewArrivals

# Create your views here.

def index(request):
    cards = Card.objects.all()
    return render(request, 'index.html', {"cards": cards} )


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def reviews(request):
    return render(request, 'reviews.html')

def buy(request):
    offers = Offers.objects.all()
    arrivals = NewArrivals.objects.all()
    return render(request, 'buy.html', {'offers' : offers, 'kids_arrivals' : arrivals})

def shop_offers(request):
    offer = Offers.objects.all()
    return render(request, 'shop_offers.html', {
        'kids_offers' : offer.filter(category='kids'),
        'men_offers' : offer.filter(category='men'),
        'women_offers' : offer.filter(category='women'),
        })
    
def new_arrivals(request):
    new_arrivals = NewArrivals.objects.all()
    return render(request, 'new_arrivals.html', {
        'kids_arrivals' : new_arrivals.filter(category='kids'),
        'men_arrivals' : new_arrivals.filter(category='men'),
        'women_arrivals' : new_arrivals.filter(category='women'),
    })
    
    
def login(request):
    return render(request , 'login.html')

def signup(request):
    return render(request, 'signup.html')

def product_detail(request, product_type, product_id):
    product = None
    product2 = None
    
    if product_type == 'offer':
        try:
            product = Offers.objects.get(id=product_id)
        except Offers.DoesNotExist:
            pass
    elif product_type == 'arrival':
        try:
            product2 = NewArrivals.objects.get(id=product_id)
        except NewArrivals.DoesNotExist:
            pass
    
    return render(request, 'product_detail.html', {'product': product, 'product2': product2})