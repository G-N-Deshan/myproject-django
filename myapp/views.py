from django.shortcuts import render
from django.http import HttpResponse
from .models import Card 

# Create your views here.

def index(request):
    cards = Card.objects.all()
    return render(request, 'index.html', {"cards": cards} )

