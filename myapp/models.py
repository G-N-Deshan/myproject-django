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
    
# Create your models here.
