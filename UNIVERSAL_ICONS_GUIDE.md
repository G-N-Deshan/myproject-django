# UNIVERSAL ICONS GUIDE - KidZone
**Purpose**: Visual clarity through contextual icons  
**Library**: Bootstrap Icons (already loaded)  
**Best Practices**: Icon + text for first impression, icon-only for repeated actions

---

## 🎨 ICON SYSTEM - Standard Usage

### ACTION ICONS
| Action | Icon | Code | Usage |
|--------|------|------|-------|
| Add/Create | `bi-plus-circle` | `<i class="bi bi-plus-circle"></i>` | Add to cart, new item |
| Edit | `bi-pencil` | `<i class="bi bi-pencil"></i>` | Edit profile, edit review |
| Delete/Remove | `bi-trash` | `<i class="bi bi-trash"></i>` | Remove from cart, delete |
| Save | `bi-check-circle` | `<i class="bi bi-check-circle"></i>` | Save changes, confirm |
| Search | `bi-search` | `<i class="bi bi-search"></i>` | Search input, search button |
| Filter | `bi-funnel` | `<i class="bi bi-funnel"></i>` | Filter products, apply filters |
| Sort | `bi-arrow-down-up` | `<i class="bi bi-arrow-down-up"></i>` | Sort products |
| Download | `bi-download` | `<i class="bi bi-download"></i>` | Download invoice, export |
| Upload | `bi-upload` | `<i class="bi bi-upload"></i>` | Upload image, file upload |
| Close/X | `bi-x-lg` | `<i class="bi bi-x-lg"></i>` | Close dialog, remove |
| Expand | `bi-chevron-down` | `<i class="bi bi-chevron-down"></i>` | Expand menu, show more |
| Collapse | `bi-chevron-up` | `<i class="bi bi-chevron-up"></i>` | Collapse menu |
| Next | `bi-chevron-right` | `<i class="bi bi-chevron-right"></i>` | Next page, forward |
| Previous | `bi-chevron-left` | `<i class="bi bi-chevron-left"></i>` | Previous page, back |

### INFORMATION ICONS
| Info | Icon | Code | Usage |
|------|------|------|-------|
| Success | `bi-check-circle-fill` | `<i class="bi bi-check-circle-fill"></i>` | Success message, order placed |
| Warning | `bi-exclamation-triangle-fill` | `<i class="bi bi-exclamation-triangle-fill"></i>` | Warning, low stock |
| Error | `bi-x-circle-fill` | `<i class="bi bi-x-circle-fill"></i>` | Error message, failed |
| Info | `bi-info-circle-fill` | `<i class="bi bi-info-circle-fill"></i>` | Information tooltip |
| Shipping | `bi-box-seam` | `<i class="bi bi-box-seam"></i>` | Shipping, delivery |
| Payment | `bi-credit-card` | `<i class="bi bi-credit-card"></i>` | Payment method |
| Location | `bi-geo-alt` | `<i class="bi bi-geo-alt"></i>` | Address, location |
| Phone | `bi-telephone` | `<i class="bi bi-telephone"></i>` | Contact, phone |
| Email | `bi-envelope` | `<i class="bi bi-envelope"></i>` | Email, message |
| Star/Rating | `bi-star-fill` | `<i class="bi bi-star-fill"></i>` | Rating, review |
| Heart/Wishlist | `bi-heart-fill` | `<i class="bi bi-heart-fill"></i>` | Favorite, wishlist |
| Cart | `bi-cart` | `<i class="bi bi-cart"></i>` | Shopping cart |

### NAVIGATION/MENU ICONS
| Nav | Icon | Code | Usage |
|-----|------|------|-------|
| Home | `bi-house-fill` | `<i class="bi bi-house-fill"></i>` | Home page |
| Products | `bi-grid-3x3` | `<i class="bi bi-grid-3x3"></i>` | Browse products |
| Categories | `bi-tag` | `<i class="bi bi-tag"></i>` | Categories |
| Profile/User | `bi-person-circle` | `<i class="bi bi-person-circle"></i>` | User profile |
| Orders | `bi-box` | `<i class="bi bi-box"></i>` | My orders |
| Reviews | `bi-chat-quote` | `<i class="bi bi-chat-quote"></i>` | Reviews |
| Settings | `bi-gear` | `<i class="bi bi-gear"></i>` | Settings |
| Help | `bi-question-circle` | `<i class="bi bi-question-circle"></i>` | Help, FAQ |
| Menu | `bi-list` | `<i class="bi bi-list"></i>` | Menu toggle |
| Bell/Notifications | `bi-bell` | `<i class="bi bi-bell"></i>` | Notifications |

---

## 📄 PAGES NEEDING ICONS

### 1. Product Pages (kids_cloths.html, women_cloths.html, mens_cloths.html)
**Needs:**
- Filter icon (funnel)
- Sort icon (arrows)
- Category badges
- Stock status icons
- Price comparison icons

### 2. Search Results (search_results.html)
**Needs:**
- Search icon in input
- Result count icon
- Empty state icon
- Popular searches

### 3. Wishlist (wishlist.html)
**Needs:**
- Heart icon for favorites
- Move to cart icon
- Remove icon
- Empty wishlist state

### 4. Cart (cart_details_page.html)
**Needs:**
- Quantity adjustment icons
- Remove item icon
- Continue shopping icon
- Checkout process steps

### 5. Orders (my_orders.html, order_tracking.html)
**Needs:**
- Order status icons
- Tracking step icons
- Delivery date icon
- Reorder icon

### 6. Reviews (reviews.html, product_detail.html)
**Needs:**
- Star rating icons
- Review helpful icon
- Report review icon
- Verified purchase badge

### 7. Profile (profile.html)
**Needs:**
- Edit profile icon
- Edit address icon
- Security/password icon
- Logout icon
- Settings icon

### 8. Payment (payment.html)
**Needs:**
- Secure/lock icon
- Card type icons
- Checkmark for steps completed
- Back icon to return

### 9. Forms (login.html, signup.html, contact.html)
**Needs:**
- Input field icons (user, password, email)
- Password visibility toggle
- Validation icons (checkmark, X)
- Form error icons

### 10. Buttons & CTAs (All pages)
**Needs:**
- Shop Now → shopping bag
- View Offers → fire/lightning
- Learn More → arrow right
- Back → arrow left
- View Details → eye icon

---

## 💡 ICON PLACEMENT RULES

### Rule 1: Icon + Text for First Interaction
```html
<!-- First time user sees action -->
<button class="btn btn-primary">
    <i class="bi bi-plus-circle"></i> Add to Cart
</button>
```

### Rule 2: Icon-Only for Repeated Actions
```html
<!-- After user understands function (in lists, tables) -->
<button class="icon-btn" aria-label="Remove item" title="Remove">
    <i class="bi bi-trash"></i>
</button>
```

### Rule 3: Status Icons Always with Text
```html
<!-- Status must be clear -->
<span>
    <i class="bi bi-check-circle-fill text-success"></i> Delivered
</span>
```

### Rule 4: Input Icons on Left
```html
<div class="input-group">
    <i class="bi bi-search input-icon"></i>
    <input type="text" placeholder="Search...">
</div>
```

---

## 🎯 COLOR CODING FOR ICONS

```css
/* Success states */
.icon-success { color: var(--color-success); }  /* Green */

/* Warning states */
.icon-warning { color: var(--color-warning); }  /* Amber */

/* Error states */
.icon-error { color: var(--color-error); }  /* Red */

/* Primary action */
.icon-primary { color: var(--color-primary); }  /* Indigo */

/* Muted/secondary */
.icon-muted { color: var(--color-text-muted); }  /* Light gray */

/* Inverse (white on dark) */
.icon-inverse { color: var(--color-text-inverse); }  /* White */
```

---

## 🔧 ICON CSS HELPERS

```css
/* Size variations */
.icon-sm { font-size: 1rem; }
.icon-md { font-size: 1.25rem; }
.icon-lg { font-size: 1.5rem; }
.icon-xl { font-size: 2rem; }

/* Spacing */
.icon-mr { margin-right: 0.5rem; }
.icon-ml { margin-left: 0.5rem; }

/* Icon button */
.icon-btn {
    border: none;
    background: transparent;
    cursor: pointer;
    padding: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    transition: all 0.2s;
}

.icon-btn:hover {
    background: var(--color-background);
    color: var(--color-primary);
}

.icon-btn:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
}

/* Input with icon */
.input-group {
    position: relative;
    display: flex;
    align-items: center;
}

.input-icon {
    position: absolute;
    left: 12px;
    color: var(--color-text-muted);
    pointer-events: none;
}

.input-group input {
    padding-left: 36px;
}

/* Spinning icon (for loading) */
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.icon-spin {
    animation: spin 1s linear infinite;
}
```

---

## ✅ IMPLEMENTATION CHECKLIST

**Product Pages:**
- [ ] Add filter icon to filter button
- [ ] Add sort icon to sort dropdown
- [ ] Add stock status badges with icons
- [ ] Add price comparison icons if applicable
- [ ] Add quantity +/- icons for product variations

**Search & Filtering:**
- [ ] Add search icon in input field
- [ ] Add funnel icon to filter button
- [ ] Add result count indicator
- [ ] Add empty state illustration/icon
- [ ] Add popular searches with icons

**Shopping Experience:**
- [ ] Add shopping bag icon to "Add to Cart"
- [ ] Add heart icon to "Add to Wishlist"
- [ ] Add trash icon to "Remove from Cart"
- [ ] Add checkmark for "Applied" filters/selections
- [ ] Add loading spinner during operations

**Checkout Flow:**
- [ ] Add step indicator icons
- [ ] Add checkmark for completed steps
- [ ] Add lock/secure icon on payment page
- [ ] Add card type icons
- [ ] Add delivery/tracking icons on order page

**User Account:**
- [ ] Add person icon to profile section
- [ ] Add edit icon to editable fields
- [ ] Add location icon to addresses
- [ ] Add phone/email icons to contact info
- [ ] Add heart icon to wishlists
- [ ] Add gear icon to settings
- [ ] Add logout icon

**Forms:**
- [ ] Add icons inside input fields (user, email, lock)
- [ ] Add password visibility toggle icon
- [ ] Add validation icons (check/X)
- [ ] Add required asterisk with tooltip icon
- [ ] Add help icon for form tips

---

## 🚀 QUICK IMPLEMENTATION PATTERN

```html
<!-- Pattern 1: Button with icon (first interaction) -->
<button class="btn btn-primary">
    <i class="bi bi-plus-circle icon-mr"></i> Add to Cart
</button>

<!-- Pattern 2: Icon-only button (repeated action) -->
<button class="icon-btn" aria-label="Remove" title="Remove from cart">
    <i class="bi bi-trash"></i>
</button>

<!-- Pattern 3: Status with icon -->
<div class="status-badge">
    <i class="bi bi-check-circle-fill icon-success icon-mr"></i> In Stock
</div>

<!-- Pattern 4: Input with icon -->
<div class="input-group">
    <i class="bi bi-search input-icon"></i>
    <input type="text" placeholder="Search products...">
</div>

<!-- Pattern 5: Link with icon -->
<a href="#filters" class="filter-link">
    <i class="bi bi-funnel icon-mr"></i> Open Filters
</a>

<!-- Pattern 6: Loading state with spinning icon -->
<button class="btn" disabled>
    <i class="bi bi-hourglass-split icon-spin icon-mr"></i> Processing...
</button>

<!-- Pattern 7: Empty state with large icon -->
<div class="empty-state">
    <i class="bi bi-inbox icon-xl icon-muted"></i>
    <p>No products found</p>
</div>
```

---

**This guide is ready to implement across all pages to significantly improve UX through visual clarity.**

