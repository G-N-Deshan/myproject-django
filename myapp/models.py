from django.db import models


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
    
    def __str__(self):
        return self.title
    
    
    
class Cloths(models.Model):
    CATEGORY_CHOICES = [
        ('kids-men', 'Kids-men'),
        ('men', 'Men'),
        ('women','Women'),
        ('kids-girl', 'Kids-girl')
    ]
    
    imageUrl = models.ImageField(upload_to='cloths/')
    name = models.CharField(max_length=150)
    price = models.CharField(max_length=50, blank=True)
    desccription = models.TextField()
    price1 = models.CharField(max_length=50, blank=True)
    price2 = models.CharField(max_length=50, blank=True)
    discount_text = models.CharField(max_length=50, blank=True) 
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='kids-men')   
    
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



from django.db import models

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

    def __str__(self):
        return self.name

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    class Meta:
        ordering = ['-created_at']