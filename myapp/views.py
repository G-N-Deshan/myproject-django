from urllib import request
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Card, Offers, NewArrivals, Cloths, Review, ContactMessage, Toy
from .forms import ReviewForm, ContactForm

# Create your views here.

def index(request):
    cards = Card.objects.all()
    return render(request, 'index.html', {"cards": cards} )


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


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


def cloths(request):
    return render(request, 'cloths.html')

def toys(request):  
    return render(request, 'toys.html')

    
def kids_cloths(request):
    kids_cloths = Cloths.objects.filter(category='kids-men')
    kids_girls_cloths = Cloths.objects.filter(category='kids-girl')
    return render(request, 'kids_cloths.html', {'kids_cloths': kids_cloths, 'kids_girls_cloths': kids_girls_cloths})

def women_cloths(request):
    women_cloths = Cloths.objects.filter(category='Women')
    return render(request, 'women_cloths.html', {'women_cloths': women_cloths})


def mens_cloths(request):
    mens_cloths = Cloths.objects.filter(category='men')
    return render(request, 'mens_cloths.html', {'mens_cloths': mens_cloths})

def reviews(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('review_success')  
    else:
        form = ReviewForm()
    
    # Get latest 20 reviews
    latest_reviews = Review.objects.all()[:20]
    
    return render(request, 'reviews.html', {'form': form, 'latest_reviews': latest_reviews})

def review_success(request):
    return render(request, 'review_success.html')


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! We received your message and will get back to you soon.')
            return redirect('contact_success')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact_success.html')


def toys_page(request):
    # Get filter parameters
    category = request.GET.get('category', 'all')
    age_range = request.GET.get('age', 'all')
    
    # Filter toys
    toys = Toy.objects.all()
    
    if category != 'all':
        toys = toys.filter(category=category)
    
    if age_range != 'all':
        toys = toys.filter(age_range=age_range)
    
    # Get featured toys
    featured_toys = Toy.objects.filter(is_bestseller=True)[:4]
    new_toys = Toy.objects.filter(is_new=True)[:4]
    
    context = {
        'toys': toys,
        'featured_toys': featured_toys,
        'new_toys': new_toys,
        'selected_category': category,
        'selected_age': age_range,
    }
    
    return render(request, 'toys.html', context)


def cart(request):
    return render(request, 'cart.html')

def cart_details(request):
    return render(request, 'cart_details_page.html')