from urllib import request
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Card, Offers, NewArrivals, Cloths, Review, ContactMessage, Toy, WishlistItem
from .forms import ReviewForm, ContactForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    offers = Offers.objects.all()
    arrivals = NewArrivals.objects.all()
    cards = Card.objects.all()
    wishlist_items = []
    wishlist_count = 0
    
    if request.user.is_authenticated:
        user_wishlist = WishlistItem.objects.filter(user=request.user)
        wishlist_count = user_wishlist.count()
        
        # Prepare wishlist data for template
        for item in user_wishlist[:6]:  # Show only first 6 items on home page
            wishlist_items.append({
                'id': item.id,
                'name': item.get_item().name,
                'price': item.get_price(),
                'image': item.get_item().imageUrl.url if item.get_item().imageUrl else '',
                'category': item.get_category(),
                'item_type': item.item_type,
            })
    
    context = {
        'cards': cards,
        'offers': offers,
        'arrivals': arrivals,
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_count,
    }
    
    return render(request, 'index.html', context)

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

@login_required(login_url='login')
def wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    
    cloth_items = wishlist_items.filter(item_type='cloth')
    toy_items = wishlist_items.filter(item_type='toy')
    
    total_count = wishlist_items.count()
    cloth_count = cloth_items.count()
    toy_count = toy_items.count()
    
    context = {
        'wishlist_items': wishlist_items,  
        'toy_items': toy_items,             
        'total_count': total_count,
        'cloth_count': cloth_count,
        'toy_count': toy_count,
    }
    
    return render(request, 'wishlist.html', context)
    
    
@login_required(login_url='login')
def add_to_wishlist(request, item_type, item_id):
    try:
        
        if item_type == 'cloth':
            item = get_object_or_404(Cloths, id=item_id)
            
            
            wishlist_item, created = WishlistItem.objects.get_or_create(
                user=request.user,
                item_type='cloth',
                cloth=item
            )
        
        elif item_type == 'toy':
            item = get_object_or_404(Toy, id=item_id)
            
            
            wishlist_item, created = WishlistItem.objects.get_or_create(
                user=request.user,
                item_type='toy',
                toy=item
            )
        
        else:
            messages.error(request, 'Invalid item type')
            return redirect('wishlist')
        
        if created:
            messages.success(request, f'✓ Added {item.name} to wishlist!')
        else:
            messages.info(request, f'{item.name} is already in your wishlist')
            
            
        return redirect('wishlist')
    
    except Cloths.DoesNotExist:
        messages.error(request, 'Cloth product not found')
        return redirect('buy')
    except Toy.DoesNotExist:
        messages.error(request, 'Toy product not found')
        return redirect('toys')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('wishlist')


@login_required(login_url='login')
def remove_from_wishlist(request, wishlist_id):
    try:
        wishlist_item = get_object_or_404(
            WishlistItem,
            id=wishlist_id,
            user=request.user
        )
        
        product_name = wishlist_item.get_item().name
        
        wishlist_item.delete()
        
        messages.success(request, f'✓ Removed {product_name} from wishlist')
    
    except WishlistItem.DoesNotExist:
        messages.error(request, 'Item not found in your wishlist')
    except Exception as e:
        messages.error(request, f'Error removing item: {str(e)}')
    
    return redirect('wishlist')


@login_required(login_url='login')
def move_to_cart(request, wishlist_id):
    
    try:
        wishlist_item = get_object_or_404(
            WishlistItem,
            id=wishlist_id,
            user=request.user
        )
        
        item = wishlist_item.get_item()
        product_name = item.name
        

        wishlist_item.delete()
        
        messages.success(request, f'✓ Moved {product_name} to cart!')
    
    except WishlistItem.DoesNotExist:
        messages.error(request, 'Item not found')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('wishlist')