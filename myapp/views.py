from django.shortcuts import render
from django.http import HttpResponse
from .models import Card 

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
    return render(request, 'buy.html')