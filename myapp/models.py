from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import re

class Card(models.Model):
    imageUrl = models.ImageField(upload_to='cards/')
    name = models.CharField(max_length=150)
    details = models.TextField()
    
    def __str__(self):
        return self.name
    
class Offers(models.Model):
    
    CATEGORY_CHOICES = [
        ('kids', 'Kids'),
        ('men', 'Men'),
        ('women', 'Women'),
    ]
    
    imageUrl = models.ImageField(upload_to='offers/')
    offers_badge = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    description = models.TextField()
    price1 = models.CharField(max_length=50, blank=True)
    price2 = models.CharField(max_length=50, blank=True)
    stock_text = models.CharField(max_length=50, blank=True)

    button_text = models.CharField(max_length=50)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='kids')
    end_time = models.DateTimeField(blank=True, null=True)
    long_description = models.TextField(blank=True, default='', help_text='Detailed description shown on the product detail page')
    features = models.TextField(blank=True, default='', help_text='Key features, one per line')
    material = models.CharField(max_length=200, blank=True, default='', help_text='e.g. 100% Cotton, Polyester blend')
    brand = models.CharField(max_length=150, blank=True, default='', help_text='Brand or collection name')
    stock_quantity = models.IntegerField(default=50, help_text='Number of units in stock')
    
    def __str__(self):
        return self.title
    
class NewArrivals(models.Model):
    
    CATEGORY_CHOICES = [
        ('kids', 'Kids'),
        ('men', 'Men'),
        ('women','Women'),
    ]
    
    imageUrl = models.ImageField(upload_to='new_arrivals/')
    offers_badge = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='kids')
    long_description = models.TextField(blank=True, default='', help_text='Detailed description shown on the product detail page')
    features = models.TextField(blank=True, default='', help_text='Key features, one per line')
    material = models.CharField(max_length=200, blank=True, default='', help_text='e.g. 100% Cotton, Polyester blend')
    brand = models.CharField(max_length=150, blank=True, default='', help_text='Brand or collection name')
    stock_quantity = models.IntegerField(default=50, help_text='Number of units in stock')
    
    def __str__(self):
        return self.title
    
class Cloths(models.Model):
    CATEGORY_CHOICES = [
        ('kids-men', 'Kids Boys'),
        ('men', 'Men'),
        ('women','Women'),
        ('kids-girl', 'Kids Girls')
    ]
    
    SUBCATEGORY_CHOICES = [
        ('', 'None'),
        ('dresses', 'Dresses'),
        ('tops', 'Tops'),
        ('pants', 'Pants'),
        ('skirts', 'Skirts'),
        ('shirts', 'Shirts'),
        ('shoes', 'Shoes'),
        ('accessories', 'Accessories'),
    ]
    
    imageUrl = models.ImageField(upload_to='cloths/')
    name = models.CharField(max_length=150)
    price = models.CharField(max_length=50, blank=True)
    desccription = models.TextField()
    price1 = models.CharField(max_length=50, blank=True)
    price2 = models.CharField(max_length=50, blank=True)
    discount_text = models.CharField(max_length=50, blank=True) 
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default='kids-men')
    subcategory = models.CharField(max_length=20, choices=SUBCATEGORY_CHOICES, blank=True, default='')
    long_description = models.TextField(blank=True, default='', help_text='Detailed description shown on the product detail page')
    features = models.TextField(blank=True, default='', help_text='Key features, one per line')
    material = models.CharField(max_length=200, blank=True, default='', help_text='e.g. 100% Cotton, Polyester blend')
    brand = models.CharField(max_length=150, blank=True, default='', help_text='Brand or collection name')
    care_instructions = models.TextField(blank=True, default='', help_text='Washing and care instructions')
    sizes_available = models.CharField(max_length=200, blank=True, default='', help_text='e.g. S, M, L, XL or 2T, 3T, 4T')
    stock_quantity = models.IntegerField(default=100, help_text='Number of units in stock')
    
    def __str__(self):
        return self.name
    
class Review(models.Model):
    RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    uploadImages = models.ImageField(upload_to='reviews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_rating_display()}"

    class Meta:
        ordering = ['-created_at']
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']

class Toy(models.Model):
    CATEGORY_CHOICES = [
        ('educational', 'Educational'),
        ('outdoor', 'Outdoor'),
        ('creative', 'Creative'),
        ('electronic', 'Electronic'),
        ('plush', 'Plush'),
        ('building', 'Building'),
    ]
    
    AGE_RANGE_CHOICES = [
        ('0-2', '0-2 years'),
        ('3-5', '3-5 years'),
        ('6-8', '6-8 years'),
        ('9-12', '9-12 years'),
        ('13+', '13+ years'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    age_range = models.CharField(max_length=10, choices=AGE_RANGE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    imageUrl = models.ImageField(upload_to='toys/')
    is_bestseller = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    created_at = models.DateTimeField(auto_now_add=True)
    long_description = models.TextField(blank=True, default='', help_text='Detailed description shown on the product detail page')
    features = models.TextField(blank=True, default='', help_text='Key features, one per line')
    material = models.CharField(max_length=200, blank=True, default='', help_text='e.g. Wood, Plastic, Plush fabric')
    brand = models.CharField(max_length=150, blank=True, default='', help_text='Brand or collection name')
    safety_info = models.TextField(blank=True, default='', help_text='Safety certifications and age warnings')
    dimensions = models.CharField(max_length=200, blank=True, default='', help_text='e.g. 30cm x 20cm x 15cm')
    stock_quantity = models.IntegerField(default=50, help_text='Number of units in stock')

    def __str__(self):
        return self.name

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    class Meta:
        ordering = ['-created_at']
        
class WishlistItem(models.Model):

    ITEM_TYPE_CHOICES = [
        ('toy', 'Toy'),
        ('cloth', 'Cloth'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    
    cloth = models.ForeignKey('Cloths', on_delete=models.CASCADE, blank=True, null=True, related_name='wishlisted_by')
    
    toy = models.ForeignKey('Toy', on_delete=models.CASCADE, blank=True, null=True, related_name='wishlisted_by')
    
    added_at = models.DateTimeField(auto_now_add=True)
    
    price_alert_enabled = models.BooleanField(default=False, help_text='Send notification when price drops')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Price when item was added to wishlist')
    alert_threshold_percent = models.IntegerField(default=10, help_text='Alert if price drops by this percentage (default 10%)')
    last_alert_sent = models.DateTimeField(blank=True, null=True, help_text='Last time price alert was sent for this item')
    
    is_shared = models.BooleanField(default=False, help_text='Include in public/shared wishlist')
    shared_at = models.DateTimeField(blank=True, null=True, help_text='When wishlist was made public')
    
    class Meta:
        unique_together = [('user', 'cloth'), ('user', 'toy'),]
        ordering = ['-added_at']
        verbose_name = 'Wishlist Item'
        verbose_name_plural = 'Wishlist Items'
        indexes = [
            models.Index(fields=['user', 'price_alert_enabled']),
            models.Index(fields=['price_alert_enabled', 'last_alert_sent']),
        ]
    
    def __str__(self):
        item = self.get_item()
        item_name = item.name if item else 'Unknown'
        return f"{self.user.username} - {item_name}"
    
    def get_item(self):
        return self.cloth if self.cloth else self.toy
    
    def get_current_price(self):
        from decimal import Decimal
        item = self.get_item()
        if not item:
            return None
        if self.item_type == 'cloth':
            price_str = item.price2 or item.price1 or item.price or '0'
            price_text = str(price_str).replace('₹', '').replace('$', '').strip()
            try:
                return Decimal(price_text)
            except:
                return Decimal('0')
        elif self.item_type == 'toy':
            return item.price
        return None
    
    def check_price_drop(self):
        if not self.price_alert_enabled or not self.original_price:
            return False
        
        current_price = self.get_current_price()
        if not current_price:
            return False
        
        threshold_amount = self.original_price * (self.alert_threshold_percent / 100)
        threshold_price = self.original_price - threshold_amount
        
        return current_price <= threshold_price
    
    def get_price_drop_percent(self):
        if not self.original_price:
            return 0
        
        current_price = self.get_current_price()
        if not current_price:
            return 0
        
        drop = self.original_price - current_price
        percent = (drop / self.original_price) * 100
        return round(percent, 1)
    
    def get_item(self):
        return self.cloth if self.cloth else self.toy
    
    def get_price(self):
        if self.item_type == 'cloth':
            return self.cloth.price2 or self.cloth.price
        else:
            return str(self.toy.price)
    
    def get_category(self):
        item = self.get_item()
        return item.get_category_display() if hasattr(item, 'get_category_display') else item.category

class WishlistShare(models.Model):
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('revoked', 'Revoked'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_wishlists')
    
    share_token = models.CharField(max_length=32, unique=True, help_text='Unique token for sharing link')
    share_url = models.URLField(blank=True, help_text='Public URL for accessing shared wishlist')
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    allow_comments = models.BooleanField(default=False, help_text='Allow viewers to comment')
    allow_suggestions = models.BooleanField(default=True, help_text='Allow viewers to suggest items')
    show_prices = models.BooleanField(default=True, help_text='Display prices in shared wishlist')
    show_created_dates = models.BooleanField(default=True, help_text='Show when items were added')
    
    expires_at = models.DateTimeField(blank=True, null=True, help_text='When shared link expires')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0, help_text='Number of times shared wishlist was viewed')
    last_viewed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Wishlist Share'
        verbose_name_plural = 'Wishlist Shares'
    
    def __str__(self):
        return f"{self.owner.username}'s shared wishlist"
    
    def is_active(self):
        if self.status != 'active':
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        return True

class PriceAlert(models.Model):
    
    ALERT_TYPE_CHOICES = [
        ('price_drop', 'Price Drop'),
        ('back_in_stock', 'Back in Stock'),
        ('price_threshold', 'Threshold Reached'),
    ]
    
    wishlist_item = models.ForeignKey(WishlistItem, on_delete=models.CASCADE, related_name='price_alerts')
    
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_drop_percent = models.DecimalField(max_digits=5, decimal_places=2)
    
    is_sent = models.BooleanField(default=False, help_text='Whether notification was sent to user')
    sent_at = models.DateTimeField(blank=True, null=True)
    
    user_viewed = models.BooleanField(default=False)
    user_purchased = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Price Alert'
        verbose_name_plural = 'Price Alerts'
        indexes = [
            models.Index(fields=['is_sent', 'wishlist_item']),
            models.Index(fields=['alert_type', 'created_at']),
        ]
    
    def __str__(self):
        item = self.wishlist_item.get_item()
        return f"{item.name if item else 'Unknown'} - {self.alert_type}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Cart for session {self.session_key}"
    
    def get_total(self):
        total = 0.0
        for item in self.items.all():
            try:
                total += float(item.get_subtotal())
            except Exception:
                continue
        return total
    
    def get_item_count(self):
        return sum(item.quantity for item in self.items.all())
    
    class Meta:
        verbose_name = 'Shopping Cart'
        verbose_name_plural = 'Shopping Carts'

class CartItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('toy', 'Toy'),
        ('cloth', 'Cloth'),
        ('offer', 'Offer'),
        ('arrival', 'New Arrival'),
    ]
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    
    cloth = models.ForeignKey('Cloths', on_delete=models.CASCADE, null=True, blank=True)
    toy = models.ForeignKey('Toy', on_delete=models.CASCADE, null=True, blank=True)
    offer = models.ForeignKey('Offers', on_delete=models.CASCADE, null=True, blank=True)
    arrival = models.ForeignKey('NewArrivals', on_delete=models.CASCADE, null=True, blank=True)
    
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        item = self.get_item()
        return f"{self.quantity}x {item.name if hasattr(item, 'name') else item.title}"
    
    def get_item(self):
        if self.cloth:
            return self.cloth
        elif self.toy:
            return self.toy
        elif self.offer:
            return self.offer
        elif self.arrival:
            return self.arrival
        return None
    
    @staticmethod
    def _to_float(value):
        if value is None:
            return 0.0
        if isinstance(value, (int, float)):
            return float(value)

        s = str(value).strip()
        if not s:
            return 0.0

        s = re.sub(r'[^0-9,.\-]', '', s).replace(',', '')
        try:
            return float(s) if s else 0.0
        except ValueError:
            return 0.0

    def get_price(self):
        item = self.get_item()
        if not item:
            return 0.0

        if self.item_type == 'cloth':
            return self._to_float(item.price2 or item.price or 0)
        elif self.item_type == 'toy':
            return self._to_float(item.price)
        elif self.item_type == 'offer':
            return self._to_float(item.price2 or item.price1 or 0)
        elif self.item_type == 'arrival':
            return self._to_float(item.price or 0)
        return 0.0
    
    def get_subtotal(self):
        return self.get_price() * self.quantity
    
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True)
    
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon_code = models.CharField(max_length=30, blank=True, default='')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, default='cash_on_delivery')
    tracking_number = models.CharField(max_length=100, blank=True, default='')
    estimated_delivery = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=200)
    item_type = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity}x {self.item_name}"

class ProductReview(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    PRODUCT_TYPE_CHOICES = [
        ('cloth', 'Cloth'),
        ('toy', 'Toy'),
        ('offer', 'Offer'),
        ('arrival', 'Arrival'),
    ]

    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES)
    cloth = models.ForeignKey('Cloths', on_delete=models.CASCADE, blank=True, null=True, related_name='product_reviews')
    toy = models.ForeignKey('Toy', on_delete=models.CASCADE, blank=True, null=True, related_name='product_reviews')
    offer = models.ForeignKey('Offers', on_delete=models.CASCADE, blank=True, null=True, related_name='product_reviews')
    arrival = models.ForeignKey('NewArrivals', on_delete=models.CASCADE, blank=True, null=True, related_name='product_reviews')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.rating}/5"

class ProductImage(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('cloth', 'Cloth'),
        ('toy', 'Toy'),
        ('offer', 'Offer'),
        ('arrival', 'Arrival'),
    ]

    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES)
    cloth = models.ForeignKey('Cloths', on_delete=models.CASCADE, blank=True, null=True, related_name='gallery_images')
    toy = models.ForeignKey('Toy', on_delete=models.CASCADE, blank=True, null=True, related_name='gallery_images')
    offer = models.ForeignKey('Offers', on_delete=models.CASCADE, blank=True, null=True, related_name='gallery_images')
    arrival = models.ForeignKey('NewArrivals', on_delete=models.CASCADE, blank=True, null=True, related_name='gallery_images')

    image = models.ImageField(upload_to='product_gallery/')
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return f"Image for {self.product_type} (order: {self.sort_order})"

class Inventory(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('cloth', 'Cloth'),
        ('toy', 'Toy'),
        ('offer', 'Offer'),
        ('arrival', 'Arrival'),
    ]

    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES)
    cloth = models.OneToOneField('Cloths', on_delete=models.CASCADE, blank=True, null=True, related_name='inventory')
    toy = models.OneToOneField('Toy', on_delete=models.CASCADE, blank=True, null=True, related_name='inventory')
    offer = models.OneToOneField('Offers', on_delete=models.CASCADE, blank=True, null=True, related_name='inventory')
    arrival = models.OneToOneField('NewArrivals', on_delete=models.CASCADE, blank=True, null=True, related_name='inventory')

    stock = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventory'

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def is_low_stock(self):
        return 0 < self.stock <= self.low_stock_threshold

    def get_product(self):
        return self.cloth or self.toy or self.offer or self.arrival

    def __str__(self):
        product = self.get_product()
        name = getattr(product, 'name', None) or getattr(product, 'title', '?')
        return f"{name} — {self.stock} in stock"

class Coupon(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]

    code = models.CharField(max_length=30, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_uses = models.PositiveIntegerField(default=0, help_text='0 = unlimited')
    used_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if now < self.valid_from or now > self.valid_until:
            return False
        if self.max_uses > 0 and self.used_count >= self.max_uses:
            return False
        return True

    def get_discount(self, subtotal):
        if self.discount_type == 'percentage':
            return round(subtotal * self.discount_value / 100, 2)
        return min(self.discount_value, subtotal)

    def __str__(self):
        return f"{self.code} — {self.discount_value}{'%' if self.discount_type == 'percentage' else ' Rs'}"

    class Meta:
        ordering = ['-created_at']

class ProductVariant(models.Model):
    cloth = models.ForeignKey('Cloths', on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=20, blank=True, help_text='e.g. S, M, L, XL')
    color = models.CharField(max_length=50, blank=True, help_text='e.g. Red, Blue')
    color_code = models.CharField(max_length=7, blank=True, help_text='e.g. #ff0000')
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['cloth', 'size', 'color']
        verbose_name = 'Product Variant'
        verbose_name_plural = 'Product Variants'

    def __str__(self):
        parts = []
        if self.size:
            parts.append(self.size)
        if self.color:
            parts.append(self.color)
        return f"{self.cloth.name} — {' / '.join(parts)}" if parts else self.cloth.name

class OrderTracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tracking_updates')
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order Tracking Update'
        verbose_name_plural = 'Order Tracking Updates'

    def __str__(self):
        return f"{self.order.order_number} → {self.get_status_display()} ({self.created_at:%Y-%m-%d %H:%M})"

class SiteUpdate(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Update Tracker'

    @classmethod
    def touch(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        obj.save()
        return obj

class BackInStockNotification(models.Model):
    ITEM_TYPE_CHOICES = [
        ('cloth', 'Clothing'),
        ('toy', 'Toy'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='back_in_stock_notifications')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    cloth = models.ForeignKey(Cloths, on_delete=models.CASCADE, null=True, blank=True, related_name='back_in_stock_notifications')
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE, null=True, blank=True, related_name='back_in_stock_notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text='Notification remains active until product is back in stock')
    notified_at = models.DateTimeField(null=True, blank=True, help_text='When the user was notified that product is back in stock')

    class Meta:
        verbose_name = 'Back in Stock Notification'
        verbose_name_plural = 'Back in Stock Notifications'
        unique_together = ('user', 'cloth', 'item_type')

    def __str__(self):
        product_name = self.cloth.name if self.cloth else self.toy.name
        return f"{self.user.username} → {product_name} (Back in Stock Alert)"

    def get_product(self):
        return self.cloth if self.cloth else self.toy

class OutOfStockReservation(models.Model):
    ITEM_TYPE_CHOICES = [
        ('cloth', 'Clothing'),
        ('toy', 'Toy'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('notified', 'Notified - Ready to Purchase'),
        ('completed', 'Completed - Purchased'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='out_of_stock_reservations')
    email = models.EmailField(help_text='Notification will be sent to this email')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    cloth = models.ForeignKey(Cloths, on_delete=models.CASCADE, null=True, blank=True, related_name='reservations')
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE, null=True, blank=True, related_name='reservations')
    quantity = models.PositiveIntegerField(default=1, help_text='How many units to reserve')
    size = models.CharField(max_length=10, blank=True, help_text='For cloths: S, M, L, XL, etc.')
    color = models.CharField(max_length=50, blank=True, help_text='Preferred color/variant')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    notified_at = models.DateTimeField(null=True, blank=True, help_text='When user was notified that product is back in stock')
    completed_at = models.DateTimeField(null=True, blank=True, help_text='When the reservation was fulfilled')
    expires_at = models.DateTimeField(null=True, blank=True, help_text='Reservation expires if not completed by this date (30 days default)')

    class Meta:
        verbose_name = 'Out of Stock Reservation'
        verbose_name_plural = 'Out of Stock Reservations'
        ordering = ('-created_at',)

    def __str__(self):
        product_name = self.cloth.name if self.cloth else self.toy.name
        return f"{self.user.username} → {product_name} x{self.quantity} ({self.get_status_display()})"

    def get_product(self):
        return self.cloth if self.cloth else self.toy

    def is_expired(self):
        if self.expires_at and self.expires_at < timezone.now():
            return True
        return False

    def mark_as_notified(self):
        self.status = 'notified'
        self.notified_at = timezone.now()
        self.save()

    def mark_as_completed(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
