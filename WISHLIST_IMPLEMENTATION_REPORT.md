# Wishlist Implementation Report

## 1. EXISTING WISHLIST SYSTEM ✅

### Database Model
**File:** [myapp/models.py](myapp/models.py#L199)

```python
class WishlistItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('toy', 'Toy'),
        ('cloth', 'Cloth'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    cloth = models.ForeignKey('Cloths', on_delete=models.CASCADE, blank=True, null=True)
    toy = models.ForeignKey('Toy', on_delete=models.CASCADE, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [('user', 'cloth'), ('user', 'toy')]
        ordering = ['-added_at']
```

**Key Features:**
- Users can only have one wishlist entry per product (unique constraint)
- Supports 2 item types: **Cloth** and **Toy**
- Tracks `added_at` timestamp
- Related to Django's `User` model via ForeignKey

### Views (Backend Routes)
**File:** [myapp/views.py](myapp/views.py#L1180)

| Function | Purpose | Auth Required |
|----------|---------|---------------|
| `wishlist()` | Display user's wishlist page | ❌ No |
| `add_to_wishlist()` | Add items to wishlist | ✅ Yes (login_required) |
| `remove_from_wishlist()` | Remove items from wishlist | ✅ Yes (login_required) |
| `move_to_cart()` | Move wishlist item to cart | ✅ Yes (login_required) |

### URL Routes
**File:** [myapp/urls.py](myapp/urls.py#L44)

```
GET    /wishlist/                                → wishlist()
GET    /wishlist/add/<item_type>/<item_id>/     → add_to_wishlist()
GET    /wishlist/remove/<wishlist_id>/          → remove_from_wishlist()
GET    /wishlist/move-to-cart/<wishlist_id>/    → move_to_cart()
```

### Frontend Template
**File:** [templates/wishlist.html](templates/wishlist.html)

**Features:**
- Hero section with 3D floating shapes (decorative)
- Tabbed interface: All / Cloths / Toys
- Grid layout for wishlist cards
- Each card shows: Image, Name, Category, Price
- Actions: "Move to Cart" & "Remove" buttons
- Empty state with CTA to browse products
- Stats showing total counts by type

### JavaScript
**File:** [static/wishlist.js](static/wishlist.js)

**Functionality:**
- Tab switching without page reload (All/Cloths/Toys)
- Alert auto-dismiss after 4 seconds
- Uses aria labels for accessibility

### CSS Styling
**File:** [static/wishlist.css](static/wishlist.css)

**Design Elements:**
- CSS variables for theming (--bg, --card, --text, --primary, --danger)
- Gradient backgrounds
- Floating animations
- Responsive grid layout
- Heartbeat and drift animations for visual polish

---

## 2. PRODUCT ID ATTRIBUTES

### Product Types & ID Systems

| Product Type | Model | Primary ID | Notes |
|--------------|-------|-----------|-------|
| **Cloths** | [Cloths](myapp/models.py#L64) | `cloth.id` (auto-increment) | Can have sizes (S, M, L, XL) |
| **Toys** | [Toy](myapp/models.py#L149) | `toy.id` (auto-increment) | Has age ranges (0-2, 3-5, etc.) |
| **Offers** | [Offers](myapp/models.py#L16) | `offer.id` | ⚠️ NOT in current wishlist system |
| **New Arrivals** | [NewArrivals](myapp/models.py#L48) | `arrival.id` | ⚠️ NOT in current wishlist system |

### Wishlist Item Type Routing
```
item_type='cloth'  → References Cloths model via cloth FK
item_type='toy'    → References Toy model via toy FK
```

**⚠️ Gap:** Offers and NewArrivals are NOT currently in wishlist system (though they ARE in cart system)

---

## 3. CART IMPLEMENTATION STRUCTURE (Reference)

### Database Model
**File:** [myapp/models.py](myapp/models.py#L245)

```python
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
```

### Key Differences from Wishlist
| Feature | Cart | Wishlist |
|---------|------|----------|
| **Quantity** | ✅ Tracked | ❌ Not tracked |
| **Item Types** | 4 (cloth, toy, offer, arrival) | 2 (cloth, toy) |
| **Session Support** | ✅ Guest carts via session_key | ❌ Auth only |
| **Unique Constraint** | ❌ Can have duplicates with qty | ✅ Only 1 per item |

### Cart Routes
```
POST   /cart/add/<item_type>/<item_id>/         → add_to_cart()
GET    /cart/                                   → cart_page()
GET    /cart/get/                               → get_cart_data() [AJAX]
PATCH  /cart/update/<cart_item_id>/             → update_cart_item()
DELETE /cart/remove/<cart_item_id>/             → remove_from_cart()
POST   /cart/clear/                             → clear_cart()
```

---

## 4. HEART BUTTON & FAVORITES UI

### 1. Quick-View Modal Integration
**File:** [static/quick-view.js](static/quick-view.js#L208-L209)

```html
<button class="qv-wishlist-btn" data-item-type="${itemType}" data-item-id="${product.id}">
    <i class="bi ${product.is_wishlisted ? 'bi-heart-fill' : 'bi-heart'}"></i>
</button>
```

**Styling:** [static/quick-view.css](static/quick-view.css#L362)

```css
.qv-wishlist-btn {
    /* Primary button styling */
}
.qv-wishlist-btn:hover {
    /* Hover effects */
}
.qv-wishlist-btn.wishlisted {
    /* Active state with filled heart icon */
}
```

### 2. Icon System
**File:** [UNIVERSAL_ICONS_GUIDE.md](UNIVERSAL_ICONS_GUIDE.md#L41)

- **Icon Class:** `bi-heart-fill` (filled) / `bi-heart` (outline)
- **Library:** Bootstrap Icons (bi-*)
- **Usage:** Displayed on wishlist buttons, product cards, comparisons

### 3. Quick-View Wishlist Toggle
**Current Implementation (Bug):**

```javascript
// static/quick-view.js line 275
async function toggleWishlist(itemType, itemId, button) {
    const response = await fetch('/api/wishlist/toggle/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            item_type: itemType,
            item_id: itemId
        })
    });
    
    if (data.added) {
        button.classList.add('wishlisted');
        button.innerHTML = '<i class="bi bi-heart-fill"></i> Wishlisted';
    }
}
```

**⚠️ ISSUE:** The endpoint `/api/wishlist/toggle/` **DOES NOT EXIST** in urls.py. This will cause 404 errors.

### 4. Product Detail Page
The `quick_view_product()` API endpoint populates the `is_wishlisted` field for products:

```python
# myapp/views.py line 2316
'is_wishlisted': WishlistItem.objects.filter(user=request.user, cloth=product).exists() 
    if request.user.is_authenticated else False,
```

---

## 5. DATABASE STRUCTURE FOR USER PREFERENCES

### User Authentication
- **Model Used:** Django's built-in `User` model from `django.contrib.auth.models`
- **Location:** [myapp/models.py](myapp/models.py#L2) imports

### Wishlist User Association
```python
user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
```

- **Authentication:** All wishlist operations require `@login_required`
- **Access Control:** Users can only see/modify their own wishlist

### Wishlist Data Storage
- **Type:** SQL Database (Django ORM - likely SQLite for development)
- **File:** [db.sqlite3](../db.sqlite3) (in project root)
- **Table:** `myapp_wishlistitem`

**Fields Stored:**
- `id` (primary key)
- `user_id` (FK to User)
- `item_type` (CharField: 'cloth' or 'toy')
- `cloth_id` (nullable FK)
- `toy_id` (nullable FK)
- `added_at` (timestamp)

### Session Management (for guests)
**File:** [myapp/views.py](myapp/views.py#L35-L48) - `get_or_create_cart()` function

```python
if not request.user.is_authenticated:
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
```

**Note:** Wishlist does NOT support anonymous users (unlike cart). Users must login to add items to wishlist.

### No localStorage Usage
- ✅ **Server-side only** - No localStorage implementation found for wishlist
- ✅ **Persistent across sessions** - Data stored in database
- ⚠️ **Requires authentication** - No anonymous wishlist support

---

## 6. QUICK VIEW PRODUCT API RESPONSE

**File:** [myapp/views.py](myapp/views.py#L2292)

### For Cloth Products
```json
{
    "id": 123,
    "item_type": "cloth",
    "name": "Cotton T-Shirt",
    "price": 29.99,
    "original_price": 39.99,
    "image": "/media/cloths/shirt.jpg",
    "description": "...",
    "sizes": ["S", "M", "L", "XL"],
    "material": "100% Cotton",
    "category": "men",
    "is_wishlisted": true,           // ← Current wishlist status
    "stock_quantity": 50,
    "stock_status": "In Stock"
}
```

### For Toy Products
```json
{
    "id": 456,
    "item_type": "toy",
    "name": "Wooden Puzzle",
    "price": 24.99,
    "original_price": 34.99,
    "discount_percentage": 28,
    "image": "/media/toys/puzzle.jpg",
    "age_range": "3-5",
    "dimensions": "30cm x 20cm",
    "is_wishlisted": false,          // ← Current wishlist status
    "stock_quantity": 100
}
```

---

## 7. SUMMARY & KEY GAPS

### ✅ Currently Implemented
1. **Database model** with user relationships
2. **View functions** for CRUD operations
3. **Complete wishlist page** with tabbed interface
4. **Move to cart** functionality
5. **Heart icon UI** in Quick-View modal
6. **Authentication checks** on protected routes
7. **Unique constraint** preventing duplicates

### ⚠️ Gaps & Issues

| Issue | File | Severity |
|-------|------|----------|
| Missing API endpoint `/api/wishlist/toggle/` | quick-view.js:275 | 🔴 HIGH |
| Offers & NewArrivals NOT in wishlist system | models.py | 🟡 MEDIUM |
| No guest/anonymous wishlist support | views.py | 🟡 MEDIUM |
| API endpoint registered but not implemented | urls.py | 🔴 HIGH |
| No wishlist comparison integration | - | 🟡 MEDIUM |

### 🎯 Recommended Next Steps
1. **Implement `/api/wishlist/toggle/` endpoint** (URGENT)
2. Extend WishlistItem to support Offers & NewArrivals
3. Add guest wishlist support (session-based like cart)
4. Integrate wishlist into product comparison
5. Add product comparison functionality to wishlist page

---

## 8. FILE LOCATIONS REFERENCE

**Core Files:**
- [Models Definition](myapp/models.py#L199) - WishlistItem class
- [View Functions](myapp/views.py#L1180) - wishlist(), add_to_wishlist(), etc.
- [URL Routes](myapp/urls.py#L44) - Endpoint patterns
- [HTML Template](templates/wishlist.html) - UI structure
- [JavaScript](static/wishlist.js) - Tab switching, alerts
- [CSS](static/wishlist.css) - Styling & animations
- [Quick View JS](static/quick-view.js#L273) - Heart button toggle (buggy)
- [Quick View CSS](static/quick-view.css#L362) - Button styling

**Supporting Files:**
- [Tests](myapp/tests.py#L92) - test_wishlist_item(), test_wishlist_add()
- [Design Guide](UNIVERSAL_ICONS_GUIDE.md#L41) - Heart icon specs
- [Feature Docs](PROJECT_FEATURES.md#L130) - Feature requirements
- [Quick View Docs](QUICK_VIEW_IMPLEMENTATION.md#L59) - Implementation notes

