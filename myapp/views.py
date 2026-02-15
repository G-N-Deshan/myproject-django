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
    return render(request, 'buy.html', {'offers' : offers})

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