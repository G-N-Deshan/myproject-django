from urllib import request
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Card, Offers, NewArrivals, Cloths, Review, ContactMessage, Toy, WishlistItem, Cart, CartItem, Order, OrderItem, ProductReview
from .forms import ReviewForm, ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal
import uuid
import re


# Helper function for cart management
def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key

        # Safe lookup + create (don't use user__isnull in get_or_create create kwargs)
        cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
        if not cart:
            cart = Cart.objects.create(session_key=session_key, user=None)

    return cart


def parse_catalog_price(raw_value):
    if raw_value is None:
        return 0.0
    text = str(raw_value).strip()
    if not text:
        return 0.0
    text = re.sub(r'[^0-9,.-]', '', text).replace(',', '')
    try:
        return float(text) if text else 0.0
    except ValueError:
        return 0.0


def parse_query_float(raw_value):
    try:
        return float(raw_value)
    except (TypeError, ValueError):
        return None


# Create your views here.

def index(request):
    offers = Offers.objects.all()
    arrivals = NewArrivals.objects.all()
    cards = Card.objects.all()
    wishlist_items = []
    wishlist_count = 0
    cart_count = 0
    
    # Get cart count
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.get_item_count()
        except Cart.DoesNotExist:
            cart_count = 0
    else:
        if request.session.session_key:
            try:
                cart = Cart.objects.get(session_key=request.session.session_key, user__isnull=True)
                cart_count = cart.get_item_count()
            except Cart.DoesNotExist:
                cart_count = 0
    
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
        'cart_count': cart_count,
    }
    
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


def buy(request):
    offers = Offers.objects.all()
    arrivals = NewArrivals.objects.all()
    
    # Get cart count
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.get_item_count()
        except Cart.DoesNotExist:
            cart_count = 0
    
    context = {
        'offers': offers,
        'kids_arrivals': arrivals,
        'cart_count': cart_count,
    }
    
    return render(request, 'buy.html', context)

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


# Authentication views
def user_login(request):
    # Check if user is being redirected from cart or other protected page
    next_url = request.GET.get('next', '')
    if next_url and 'cart' in next_url.lower():
        # Show info message only when coming from cart
        pass  # Message will be shown after POST if login fails
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Transfer session cart to user cart
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            
            try:
                session_cart = Cart.objects.get(session_key=session_key, user__isnull=True)
                user_cart, created = Cart.objects.get_or_create(user=user)
                
                # Move items from session cart to user cart
                for item in session_cart.items.all():
                    item.cart = user_cart
                    item.save()
                
                session_cart.delete()
            except Cart.DoesNotExist:
                pass
            
            next_url = request.POST.get('next', 'index')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    
    # Show message if coming from cart
    if 'cart' in next_url.lower():
        messages.info(request, 'Please login to view your cart')
    
    return render(request, 'login.html')


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'signup.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        auth_login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('index')
    
    return render(request, 'signup.html')


def user_logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('index')


def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to view your profile')
        return redirect('login')
    
    # Get user's order count
    order_count = Order.objects.filter(user=request.user).count()
    
    # Get user's review count (reviews by this user's email or name)
    review_count = Review.objects.filter(email=request.user.email).count()
    
    # Get user's wishlist count
    wishlist_count = WishlistItem.objects.filter(user=request.user).count()
    
    # Get recent reviews by user
    user_reviews = Review.objects.filter(email=request.user.email)[:5]
    
    # Get cart count for navigation
    cart_count = 0
    try:
        cart = Cart.objects.get(user=request.user)
        cart_count = cart.get_item_count()
    except Cart.DoesNotExist:
        cart_count = 0
    
    # Calculate satisfaction (mock - could be based on actual data)
    satisfaction = "98%"
    if order_count == 0:
        satisfaction = "N/A"
    
    context = {
        'order_count': order_count,
        'review_count': review_count,
        'wishlist_count': wishlist_count,
        'user_reviews': user_reviews,
        'cart_count': cart_count,
        'satisfaction': satisfaction,
    }
    
    return render(request, 'profile.html', context)

def product_detail(request, product_type, product_id):
    product = None
    back_url = '/'
    back_label = 'Home'
    category_label = ''
    related_products = []
    cart_count = 0

    # Get cart count
    cart = get_or_create_cart(request)
    cart_count = cart.get_item_count()

    # ── Fetch the product ──
    if product_type == 'offer':
        product = get_object_or_404(Offers, id=product_id)
        back_url = '/shop-offers/'
        back_label = 'Shop Offers'
        category_label = product.get_category_display() if product.category else 'Offer'
        related_products = list(
            Offers.objects.filter(category=product.category).exclude(id=product.id)[:4]
        )
    elif product_type == 'arrival':
        product = get_object_or_404(NewArrivals, id=product_id)
        back_url = '/new_arrivals/'
        back_label = 'New Arrivals'
        category_label = product.get_category_display() if product.category else 'Arrival'
        related_products = list(
            NewArrivals.objects.filter(category=product.category).exclude(id=product.id)[:4]
        )
    elif product_type == 'toy':
        product = get_object_or_404(Toy, id=product_id)
        back_url = '/toys/'
        back_label = 'Toys'
        category_label = product.get_category_display()
        related_products = list(
            Toy.objects.filter(category=product.category).exclude(id=product.id)[:4]
        )
    elif product_type == 'cloth':
        product = get_object_or_404(Cloths, id=product_id)
        cat = product.category
        if cat in ('kids-men', 'kids-girl'):
            back_url = '/kids_cloths/'
            back_label = 'Kids Cloths'
        elif cat == 'women':
            back_url = '/women_cloths/'
            back_label = "Women's Cloths"
        else:
            back_url = '/mens_cloths/'
            back_label = "Men's Cloths"
        category_label = product.get_category_display()
        related_products = list(
            Cloths.objects.filter(category=product.category).exclude(id=product.id)[:4]
        )
    else:
        messages.error(request, 'Invalid product type')
        return redirect('index')

    # ── Reviews ──
    fk_field = product_type  # FK field name matches product_type: cloth, toy, offer, arrival
    reviews = ProductReview.objects.filter(product_type=product_type, **{fk_field: product})
    review_count = reviews.count()
    avg_rating = 0
    if review_count:
        avg_rating = round(sum(r.rating for r in reviews) / review_count, 1)
    rating_dist = {i: reviews.filter(rating=i).count() for i in range(5, 0, -1)}

    # ── Handle review POST ──
    review_error = ''
    if request.method == 'POST':
        r_name = request.POST.get('reviewer_name', '').strip()
        r_rating = request.POST.get('review_rating')
        r_title = request.POST.get('review_title', '').strip()
        r_comment = request.POST.get('review_comment', '').strip()
        if r_name and r_rating and r_comment:
            ProductReview.objects.create(
                product_type=product_type,
                **{fk_field: product},
                user=request.user if request.user.is_authenticated else None,
                name=r_name,
                rating=int(r_rating),
                title=r_title,
                comment=r_comment,
            )
            return redirect('product_detail', product_type=product_type, product_id=product_id)
        else:
            review_error = 'Please fill in your name, rating, and comment.'

    # ── Check wishlist ──
    in_wishlist = False
    if request.user.is_authenticated and product_type in ('cloth', 'toy'):
        fk = {'cloth': product} if product_type == 'cloth' else {'toy': product}
        in_wishlist = WishlistItem.objects.filter(user=request.user, **fk).exists()

    # Normalize name (Offers/NewArrivals use 'title', Cloths/Toy use 'name')
    product_name = getattr(product, 'name', '') or getattr(product, 'title', '')

    # Normalize description (Cloths model has typo 'desccription')
    product_description = getattr(product, 'description', '') or getattr(product, 'desccription', '')

    # Rich detail fields for the Detail tab
    long_description = getattr(product, 'long_description', '') or ''
    features_raw = getattr(product, 'features', '') or ''
    features_list = [f.strip() for f in features_raw.split('\n') if f.strip()] if features_raw else []
    material = getattr(product, 'material', '') or ''
    care_instructions = getattr(product, 'care_instructions', '') or ''
    sizes_available = getattr(product, 'sizes_available', '') or ''
    safety_info = getattr(product, 'safety_info', '') or ''
    dimensions = getattr(product, 'dimensions', '') or ''

    return render(request, 'product_detail.html', {
        'product': product,
        'product_type': product_type,
        'product_name': product_name,
        'product_description': product_description,
        'back_url': back_url,
        'back_label': back_label,
        'category_label': category_label,
        'related_products': related_products,
        'reviews': reviews,
        'review_count': review_count,
        'avg_rating': avg_rating,
        'rating_dist': rating_dist,
        'review_error': review_error,
        'in_wishlist': in_wishlist,
        'cart_count': cart_count,
        'long_description': long_description,
        'features_list': features_list,
        'material': material,
        'care_instructions': care_instructions,
        'sizes_available': sizes_available,
        'safety_info': safety_info,
        'dimensions': dimensions,
    })


def cloths(request):
    return render(request, 'cloths.html')

def toys(request):  
    return render(request, 'toys.html')

    
def kids_cloths(request):
    def parse_price(raw_value):
        if raw_value is None:
            return 0.0
        text = str(raw_value).strip()
        if not text:
            return 0.0
        text = re.sub(r'[^0-9,.-]', '', text).replace(',', '')
        try:
            return float(text) if text else 0.0
        except ValueError:
            return 0.0

    def parse_float(raw_value):
        try:
            return float(raw_value)
        except (TypeError, ValueError):
            return None

    gender = request.GET.get('gender', 'all')
    subcategory = request.GET.get('subcategory', 'all')
    sort = request.GET.get('sort', 'featured')
    min_price = parse_float(request.GET.get('min_price'))
    max_price = parse_float(request.GET.get('max_price'))
    search = request.GET.get('q', '').strip()

    kids_queryset = Cloths.objects.filter(category__in=['kids-men', 'kids-girl'])

    if gender in ['kids-men', 'kids-girl']:
        kids_queryset = kids_queryset.filter(category=gender)

    if subcategory and subcategory != 'all':
        kids_queryset = kids_queryset.filter(subcategory=subcategory)

    if search:
        kids_queryset = kids_queryset.filter(name__icontains=search)

    all_filtered_items = list(kids_queryset)

    for item in all_filtered_items:
        item.numeric_price = parse_price(item.price2 or item.price1 or item.price)

    if min_price is not None:
        all_filtered_items = [item for item in all_filtered_items if item.numeric_price >= min_price]
    if max_price is not None:
        all_filtered_items = [item for item in all_filtered_items if item.numeric_price <= max_price]

    if sort == 'price_asc':
        all_filtered_items.sort(key=lambda item: item.numeric_price)
    elif sort == 'price_desc':
        all_filtered_items.sort(key=lambda item: item.numeric_price, reverse=True)
    elif sort == 'name_asc':
        all_filtered_items.sort(key=lambda item: item.name.lower())
    elif sort == 'name_desc':
        all_filtered_items.sort(key=lambda item: item.name.lower(), reverse=True)
    elif sort == 'newest':
        all_filtered_items.sort(key=lambda item: item.id, reverse=True)
    elif sort == 'oldest':
        all_filtered_items.sort(key=lambda item: item.id)
    else:
        all_filtered_items.sort(key=lambda item: item.id, reverse=True)

    kids_girls_cloths = [item for item in all_filtered_items if item.category == 'kids-girl']
    kids_cloths = [item for item in all_filtered_items if item.category == 'kids-men']

    cart_count = 0
    try:
        cart_count = get_or_create_cart(request).get_item_count()
    except Exception:
        cart_count = 0

    subcategory_options = [
        option for option in Cloths.SUBCATEGORY_CHOICES if option[0]
    ]

    return render(request, 'kids_cloths.html', {
        'kids_cloths': kids_cloths,
        'kids_girls_cloths': kids_girls_cloths,
        'all_kids_cloths': all_filtered_items,
        'selected_gender': gender,
        'selected_subcategory': subcategory,
        'selected_sort': sort,
        'selected_min_price': request.GET.get('min_price', ''),
        'selected_max_price': request.GET.get('max_price', ''),
        'search_query': search,
        'subcategory_options': subcategory_options,
        'cart_count': cart_count,
    })

def women_cloths(request):
    base_queryset = Cloths.objects.filter(category='women')

    search = request.GET.get('q', '').strip()
    subcategory = request.GET.get('subcategory', 'all')
    sort = request.GET.get('sort', 'featured')
    min_price = parse_query_float(request.GET.get('min_price'))
    max_price = parse_query_float(request.GET.get('max_price'))

    filtered = base_queryset
    if search:
        filtered = filtered.filter(name__icontains=search)
    if subcategory and subcategory != 'all':
        filtered = filtered.filter(subcategory=subcategory)

    products = list(filtered)
    for product in products:
        product.numeric_price = parse_catalog_price(product.price2 or product.price1 or product.price)

    if min_price is not None:
        products = [product for product in products if product.numeric_price >= min_price]
    if max_price is not None:
        products = [product for product in products if product.numeric_price <= max_price]

    if sort == 'price_asc':
        products.sort(key=lambda item: item.numeric_price)
    elif sort == 'price_desc':
        products.sort(key=lambda item: item.numeric_price, reverse=True)
    elif sort == 'name_asc':
        products.sort(key=lambda item: item.name.lower())
    elif sort == 'name_desc':
        products.sort(key=lambda item: item.name.lower(), reverse=True)
    elif sort == 'oldest':
        products.sort(key=lambda item: item.id)
    else:
        products.sort(key=lambda item: item.id, reverse=True)

    sections_map = {}
    for item in products:
        slug = item.subcategory if item.subcategory else 'styles'
        label = item.get_subcategory_display() if item.subcategory else 'Featured Styles'
        if slug not in sections_map:
            sections_map[slug] = {
                'slug': slug,
                'label': label,
                'items': [],
            }
        sections_map[slug]['items'].append(item)

    sections = list(sections_map.values())
    sections.sort(key=lambda entry: entry['label'].lower())

    subcategory_values = set(base_queryset.values_list('subcategory', flat=True))
    filter_subcategories = [
        option for option in Cloths.SUBCATEGORY_CHOICES
        if option[0] and option[0] in subcategory_values
    ]

    cart_count = 0
    try:
        cart_count = get_or_create_cart(request).get_item_count()
    except Exception:
        cart_count = 0

    return render(request, 'women_cloths.html', {
        'women_cloths': products,
        'sections': sections,
        'filter_subcategories': filter_subcategories,
        'selected_subcategory': subcategory,
        'selected_sort': sort,
        'selected_min_price': request.GET.get('min_price', ''),
        'selected_max_price': request.GET.get('max_price', ''),
        'search_query': search,
        'cart_count': cart_count,
    })


def mens_cloths(request):
    base_queryset = Cloths.objects.filter(category='men')

    search = request.GET.get('q', '').strip()
    subcategory = request.GET.get('subcategory', 'all')
    sort = request.GET.get('sort', 'featured')
    min_price = parse_query_float(request.GET.get('min_price'))
    max_price = parse_query_float(request.GET.get('max_price'))

    filtered = base_queryset
    if search:
        filtered = filtered.filter(name__icontains=search)
    if subcategory and subcategory != 'all':
        filtered = filtered.filter(subcategory=subcategory)

    products = list(filtered)
    for product in products:
        product.numeric_price = parse_catalog_price(product.price2 or product.price1 or product.price)

    if min_price is not None:
        products = [product for product in products if product.numeric_price >= min_price]
    if max_price is not None:
        products = [product for product in products if product.numeric_price <= max_price]

    if sort == 'price_asc':
        products.sort(key=lambda item: item.numeric_price)
    elif sort == 'price_desc':
        products.sort(key=lambda item: item.numeric_price, reverse=True)
    elif sort == 'name_asc':
        products.sort(key=lambda item: item.name.lower())
    elif sort == 'name_desc':
        products.sort(key=lambda item: item.name.lower(), reverse=True)
    elif sort == 'oldest':
        products.sort(key=lambda item: item.id)
    else:
        products.sort(key=lambda item: item.id, reverse=True)

    sections_map = {}
    for item in products:
        slug = item.subcategory if item.subcategory else 'styles'
        label = item.get_subcategory_display() if item.subcategory else 'Featured Styles'
        if slug not in sections_map:
            sections_map[slug] = {
                'slug': slug,
                'label': label,
                'items': [],
            }
        sections_map[slug]['items'].append(item)

    sections = list(sections_map.values())
    sections.sort(key=lambda entry: entry['label'].lower())

    subcategory_values = set(base_queryset.values_list('subcategory', flat=True))
    filter_subcategories = [
        option for option in Cloths.SUBCATEGORY_CHOICES
        if option[0] and option[0] in subcategory_values
    ]

    cart_count = 0
    try:
        cart_count = get_or_create_cart(request).get_item_count()
    except Exception:
        cart_count = 0

    return render(request, 'mens_cloths.html', {
        'mens_cloths': products,
        'sections': sections,
        'filter_subcategories': filter_subcategories,
        'selected_subcategory': subcategory,
        'selected_sort': sort,
        'selected_min_price': request.GET.get('min_price', ''),
        'selected_max_price': request.GET.get('max_price', ''),
        'search_query': search,
        'cart_count': cart_count,
    })

def reviews(request):
    cart_count = 0
    try:
        cart_count = get_or_create_cart(request).get_item_count()
    except Exception:
        cart_count = 0

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
    
    return render(request, 'reviews.html', {'form': form, 'latest_reviews': latest_reviews, 'cart_count': cart_count})

def review_success(request):
    return render(request, 'review_success.html')


def contact_us(request):
    cart_count = 0
    try:
        cart_count = get_or_create_cart(request).get_item_count()
    except Exception:
        cart_count = 0

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! We received your message and will get back to you soon.')
            return redirect('contact_success')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {
        'form': form,
        'cart_count': cart_count,
    })

def contact_success(request):
    cart_count = 0
    try:
        cart_count = get_or_create_cart(request).get_item_count()
    except Exception:
        cart_count = 0

    return render(request, 'contact_success.html', {
        'cart_count': cart_count,
    })


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


# Cart views
def cart_page(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    items_data = []
    for item in cart_items:
        product = item.get_item()
        items_data.append({
            'id': item.id,
            'name': product.name if hasattr(product, 'name') else product.title,
            'price': item.get_price(),
            'quantity': item.quantity,
            'subtotal': item.get_subtotal(),
            'image': product.imageUrl.url if product.imageUrl else '',
            'item_type': item.item_type,
        })
    
    context = {
        'cart_items': items_data,
        'cart_count': cart.get_item_count(),
        'subtotal': cart.get_total(),
        'tax': cart.get_total() * Decimal('0.1'),
        'total': cart.get_total() * Decimal('1.1'),
    }
    
    return render(request, 'cart.html', context)


def _wants_json(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', '')

def add_to_cart(request, item_type, item_id):
    try:
        cart = get_or_create_cart(request)
        
        # Get the product based on item_type
        item = None
        if item_type == 'cloth':
            item = get_object_or_404(Cloths, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                item_type='cloth',
                cloth=item,
                defaults={'quantity': 1}
            )
        elif item_type == 'toy':
            item = get_object_or_404(Toy, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                item_type='toy',
                toy=item,
                defaults={'quantity': 1}
            )
        elif item_type == 'offer':
            item = get_object_or_404(Offers, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                item_type='offer',
                offer=item,
                defaults={'quantity': 1}
            )
        elif item_type == 'arrival':
            item = get_object_or_404(NewArrivals, id=item_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                item_type='arrival',
                arrival=item,
                defaults={'quantity': 1}
            )
        else:
            if _wants_json(request):
                return JsonResponse({'success': False, 'error': 'Invalid item type'}, status=400)
            messages.error(request, 'Invalid item type')
            return redirect(request.META.get('HTTP_REFERER', 'index'))

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        item_name = item.name if hasattr(item, 'name') else item.title
        success_msg = f'✓ Added {item_name} to cart!'

        if request.method == 'POST' or _wants_json(request):
            return JsonResponse({
                'success': True,
                'message': success_msg,
                'cart_count': cart.get_item_count(),
                'cart_total': float(cart.get_total())
            })

        messages.success(request, success_msg)
        return redirect(request.META.get('HTTP_REFERER', 'cart'))

    except Exception as e:
        if request.method == 'POST' or _wants_json(request):
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
        messages.error(request, f'Error: {str(e)}')
        return redirect(request.META.get('HTTP_REFERER', 'index'))


@require_POST
def update_cart_item(request, cart_item_id):
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            return JsonResponse({'success': False, 'error': 'Quantity must be at least 1'}, status=400)
        
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart updated',
            'cart_count': cart.get_item_count(),
            'cart_total': float(cart.get_total()),
            'item_subtotal': float(cart_item.get_subtotal())
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def remove_from_cart(request, cart_item_id):
    try:
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
        
        item = cart_item.get_item()
        item_name = item.name if hasattr(item, 'name') else item.title
        
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Removed {item_name} from cart',
            'cart_count': cart.get_item_count(),
            'cart_total': float(cart.get_total())
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def clear_cart(request):
    try:
        cart = get_or_create_cart(request)
        cart.items.all().delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart cleared',
            'cart_count': 0,
            'cart_total': 0
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def get_cart_data(request):
    """API endpoint to get cart data as JSON"""
    try:
        cart = get_or_create_cart(request)
        items_data = []

        for item in cart.items.all():
            try:
                product = item.get_item()
                if not product:
                    continue
                product_name = product.name if hasattr(product, 'name') else product.title
                product_url = f'/product/{item.item_type}/{product.id}/'
                items_data.append({
                    'id': item.id,
                    'name': product_name,
                    'price': float(item.get_price()),
                    'quantity': int(item.quantity),
                    'subtotal': float(item.get_subtotal()),
                    'image': product.imageUrl.url if getattr(product, 'imageUrl', None) else '',
                    'item_type': item.item_type,
                    'product_url': product_url,
                })
            except Exception:
                continue

        subtotal = float(cart.get_total())
        tax = round(subtotal * 0.1, 2)
        total = round(subtotal + tax, 2)

        return JsonResponse({
            'success': True,
            'items': items_data,
            'cart_count': cart.get_item_count(),
            'subtotal': round(subtotal, 2),
            'tax': tax,
            'total': total
        })

    except Exception as e:
        return JsonResponse({
            'success': True,  # keep frontend alive, show empty cart instead of breaking
            'items': [],
            'cart_count': 0,
            'subtotal': 0.0,
            'tax': 0.0,
            'total': 0.0,
            'error': str(e),
        })


def cart_details(request):
    cart = get_or_create_cart(request)
    return render(request, 'cart_details_page.html', {
        'cart': cart,
        'cart_count': cart.get_item_count(),
    })


# Wishlist views
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
        
        # Add to cart
        cart = get_or_create_cart(request)
        
        if wishlist_item.item_type == 'cloth':
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                item_type='cloth',
                cloth=wishlist_item.cloth,
                defaults={'quantity': 1}
            )
        elif wishlist_item.item_type == 'toy':
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                item_type='toy',
                toy=wishlist_item.toy,
                defaults={'quantity': 1}
            )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        # Remove from wishlist
        wishlist_item.delete()
        
        messages.success(request, f'✓ Moved {product_name} to cart!')
    
    except WishlistItem.DoesNotExist:
        messages.error(request, 'Item not found')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('wishlist')


# Checkout and Order views
@login_required(login_url='login')
def checkout(request):
    cart = get_or_create_cart(request)
    
    if cart.get_item_count() == 0:
        messages.warning(request, 'Your cart is empty')
        return redirect('cart_details')
    
    if request.method == 'POST':
        # Validate required fields
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        country = request.POST.get('country', '').strip()
        payment_method = request.POST.get('payment_method', 'cash_on_delivery')
        
        # Check all required fields are filled
        if not all([full_name, email, phone, address, city, postal_code, country]):
            messages.error(request, 'Please fill in all required fields')
            return render(request, 'checkout.html', {
                'cart': cart,
                'cart_items': cart.items.all(),
                'subtotal': float(Decimal(str(cart.get_total()))),
                'tax': float(Decimal(str(cart.get_total())) * Decimal('0.10')),
                'shipping': 10.00,
                'total': float(Decimal(str(cart.get_total())) * Decimal('1.10') + Decimal('10.00'))
            })
        
        try:
            # Create order
            order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            
            subtotal = Decimal(str(cart.get_total()))
            tax = subtotal * Decimal('0.10')
            shipping = Decimal('10.00')
            total = subtotal + tax + shipping
            
            order = Order.objects.create(
                user=request.user,
                order_number=order_number,
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                postal_code=postal_code,
                country=country,
                subtotal=subtotal,
                tax=tax,
                shipping=shipping,
                total=total,
                payment_method=payment_method
            )
            
            # Create order items
            for cart_item in cart.items.all():
                item = cart_item.get_item()
                item_name = item.name if hasattr(item, 'name') else item.title
                OrderItem.objects.create(
                    order=order,
                    item_name=item_name,
                    item_type=cart_item.item_type,
                    quantity=cart_item.quantity,
                    price=Decimal(str(cart_item.get_price())),
                    subtotal=Decimal(str(cart_item.get_subtotal()))
                )
            
            # Clear cart
            cart.items.all().delete()
            
            messages.success(request, f'Order {order_number} placed successfully!')
            return redirect('order_success', order_number=order_number)
        
        except Exception as e:
            messages.error(request, f'Error creating order: {str(e)}')
            return render(request, 'checkout.html', {
                'cart': cart,
                'cart_items': cart.items.all(),
                'subtotal': float(Decimal(str(cart.get_total()))),
                'tax': float(Decimal(str(cart.get_total())) * Decimal('0.10')),
                'shipping': 10.00,
                'total': float(Decimal(str(cart.get_total())) * Decimal('1.10') + Decimal('10.00'))
            })
    
    # GET request - show checkout form
    subtotal = Decimal(str(cart.get_total()))
    tax = subtotal * Decimal('0.10')
    shipping = Decimal('10.00')
    total = subtotal + tax + shipping
    
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
        'subtotal': float(subtotal),
        'tax': float(tax),
        'shipping': float(shipping),
        'total': float(total)
    }
    
    return render(request, 'checkout.html', context)


@login_required(login_url='login')
def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
        'order_items': order.items.all()
    }
    
    return render(request, 'order_success.html', context)


# Profile Management Views
@login_required(login_url='login')
def update_profile(request):
    """AJAX endpoint to update user profile"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Update user fields
            user = request.user
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
            if 'email' in data:
                # Check if email is already taken by another user
                if User.objects.exclude(pk=user.pk).filter(email=data['email']).exists():
                    return JsonResponse({'success': False, 'error': 'Email already in use'}, status=400)
                user.email = data['email']
            user.save()
            
            return JsonResponse({'success': True, 'message': 'Profile updated successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required(login_url='login')
def change_password(request):
    """AJAX endpoint to change user password"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            current_password = data.get('current_password', '')
            new_password = data.get('new_password', '')
            confirm_password = data.get('confirm_password', '')
            
            user = request.user
            
            # Verify current password
            if not user.check_password(current_password):
                return JsonResponse({'success': False, 'error': 'Current password is incorrect'}, status=400)
            
            # Check password match
            if new_password != confirm_password:
                return JsonResponse({'success': False, 'error': 'New passwords do not match'}, status=400)
            
            # Check password length
            if len(new_password) < 6:
                return JsonResponse({'success': False, 'error': 'Password must be at least 6 characters'}, status=400)
            
            # Set new password
            user.set_password(new_password)
            user.save()
            
            # Re-authenticate user to keep them logged in
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
            
            return JsonResponse({'success': True, 'message': 'Password changed successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required(login_url='login')
def notification_preferences(request):
    """AJAX endpoint to update notification preferences"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Store notification preferences in session (or could use a UserProfile model)
            request.session['notify_orders'] = data.get('notify_orders', True)
            request.session['notify_promotions'] = data.get('notify_promotions', True)
            request.session['notify_new_arrivals'] = data.get('notify_new_arrivals', True)
            request.session['notify_reviews'] = data.get('notify_reviews', True)
            
            return JsonResponse({'success': True, 'message': 'Notification preferences updated!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    # GET request - return current preferences
    preferences = {
        'notify_orders': request.session.get('notify_orders', True),
        'notify_promotions': request.session.get('notify_promotions', True),
        'notify_new_arrivals': request.session.get('notify_new_arrivals', True),
        'notify_reviews': request.session.get('notify_reviews', True),
    }
    return JsonResponse({'success': True, 'preferences': preferences})


@login_required(login_url='login')
def update_email(request):
    """AJAX endpoint to update user email"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_email = data.get('email', '').strip()
            
            if not new_email:
                return JsonResponse({'success': False, 'error': 'Email is required'}, status=400)
            
            # Validate email format
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, new_email):
                return JsonResponse({'success': False, 'error': 'Invalid email format'}, status=400)
            
            user = request.user
            
            # Check if email is already taken
            if User.objects.exclude(pk=user.pk).filter(email=new_email).exists():
                return JsonResponse({'success': False, 'error': 'Email already in use'}, status=400)
            
            user.email = new_email
            user.save()
            
            return JsonResponse({'success': True, 'message': 'Email updated successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
