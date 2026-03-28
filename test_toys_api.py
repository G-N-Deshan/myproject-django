#!/usr/bin/env python
import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Toy

print(f"Toy count: {Toy.objects.count()}")

if Toy.objects.exists():
    toy = Toy.objects.first()
    print(f"First toy: {toy.name}")
    print(f"Has rating: {hasattr(toy, 'rating')}")
    print(f"Rating value: {toy.rating}")
    print(f"Price: {toy.price}")
else:
    print("No toys found in database")

# Try to test the api function directly (without exception handling)
print("\n--- Testing API Directly ---")
from myapp.views import api_load_products
from django.test import RequestFactory

factory = RequestFactory()
request = factory.get('/api/load-products/toys/?page=1')

# Call the function directly to get full traceback
response = api_load_products(request, 'toys')
print(f"API Response Status: {response.status_code}")
print(f"API Response Content: {response.content.decode()}")

