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
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='kids' )
    def __str__(self):
        return self.title
    
# Create your models here.
