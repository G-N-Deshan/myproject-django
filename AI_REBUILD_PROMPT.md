# 🚀 KidZone V2: Ultimate Rebuild Prompt (PHP & 3D Interactive Stack)
*(Copy everything below the line and paste it into the other AI model)*

---

**Act as an expert Full-Stack Software Engineer and UI/UX Designer specializing in PHP, MySQL, TailwindCSS, jQuery, and advanced Front-End 3D graphics (Three.js/Spline).**

I am completely rebuilding my e-commerce project called "KidZone" into a custom, highly-optimized PHP stack. It must be production-ready, flawlessly interactive, and maintain an ultra-premium professional standard to maximize e-commerce conversion rates.

### 1. 🛠 Target Technology Stack
*   **Backend:** Object-Oriented PHP 8+ (Custom MVC architecture heavily recommended).
*   **Database:** MySQL (Relational database designed for high scalability).
*   **Frontend Logic:** Vanilla JavaScript & jQuery (for ultra-smooth, instant AJAX requests).
*   **Styling:** TailwindCSS alongside custom CSS.
*   **3D Graphics & Animations:** Three.js, Spline, or WebGL to handle 3D background animations and interactive 3D product models.

### 2. 🎨 Elite UI/UX & Design Requirements
*   **Theme:** A clean, consistent, and premium **Light Color Theme** across the entire project. Consistency is critical.
*   **3D Elements & Animations (Crucial Requirement):** Integrate 3D models and 3D background animations on every page. This is required to increase user interactivity and elite professionalism. (e.g., a slow, elegant 3D background animation on the landing page).
*   **Heavy Imagery Focus:** Strategic use of ultra-high-quality images. Use engaging hero background images, dynamic cart product thumbnails, and interactive image galleries with zoom functionality.
*   **Professional Typography:** Use a premium pairing of multiple different fonts to maintain a professional look while promoting readability. e.g., a bold, elegant font for headings ('Playfair Display', 'Outfit'), paired with a highly clean font like 'Inter' for body text.

---

### 3. ⚙️ Exhaustive Feature Specification
You must architect and build every single one of the following features. Do not miss any of them:

#### A. Comprehensive Product Catalog
*   **Clothes Catalog:** Must include categories (Men, Women, Kids-Boys, Kids-Girls), subcategories (Dresses, Tops, Pants, Skirts, Shirts, Shoes), washing/care instructions, and material lists.
*   **Toys Catalog:** Must include categories (Educational, Outdoor, Creative, Electronic, Plush, Building), strict Age Ranges (0-2, 3-5, etc.), dimensions, and safety/certification info.
*   **Special Sections:** Dedicated Logic for 'Offers' (tracking End Times and multi-tier discount pricing) and 'New Arrivals'.
*   **Product Variants:** Users can select Size and Color codes (visually showing the color hex). Variants must dynamically affect the item price and stock.
*   **Product Gallery:** Every product supports multiple images uploaded, configured by a `sort_order` and `alt_text`.

#### B. Inventory & Advanced Stock Management
*   **Inventory Records:** Track absolute `stock_count`, `SKU`, and `low_stock_threshold` for every individual product or its variants. Admin gets notified when stock is below the threshold.
*   **Back-In-Stock Subscriptions:** If an item is out of stock, users can enter their email to subscribe. The system emails them via a cron/background job when stock is updated.
*   **Out of Stock Reservations:** A full pre-order system allowing users to reserve out-of-stock items, spanning statuses from `Pending` -> `Notified (Ready to Purchase)` -> `Completed / Cancelled`.

#### C. Shopping Cart & Dynamic Interactions
*   **Dynamic AJAX Cart:** An instant cart that slides out from the side. Never reload the page to add, update quantity, or remote an item.
*   **Guest & Authenticated Carts:** The cart must work via Session Keys for logged-out users, and merge into their User Account when they log in.

#### D. Wishlist & Price Monitoring
*   **Advanced Wishlist:** Users can add items across any category to a wishlist.
*   **Wishlist Sharing:** Users can generate a unique `share_token` (public URL) for their wishlist, with settings to `show_prices`, `allow_suggestions`, and toggle an `expires_at` date.
*   **Price Drop Alerts:** Users can enable "Price Alerts" on wishlisted items, setting a threshold (e.g., alert if drops by 10%). The system must log original prices and alert the user if the new price crosses the threshold percentage.

#### E. Checkout, Coupons & Order Workflow
*   **Coupons Engine:** Dynamic coupons that enforce `min_order_amount`, maximum usage counts (`max_uses`), and exact `valid_from` / `valid_until` dates. Support both `percentage` and `fixed amount` discounts.
*   **Multi-Step Checkout:** Address collection, subtotal, dynamic tax calculations, shipping fee logic, and total.
*   **Payment Gateway:** Architect the checkout to safely integrate a modern payment SDK like Stripe or PayPal.
*   **Granular Order Tracking:** A `OrderTracking` log for every order. As the admin changes the order status, it creates time-stamped history logs (e.g., "Package left facility") visible to the user on their dashboard.

#### F. User Interactions
*   **Advanced User Reviews:** Customers can leave 1-to-5 star ratings, write text reviews, AND upload images of the product they received.
*   **Contact System:** A dedicated contact messaging table with `is_read` toggles for the admin to follow up on client questions.

#### G. Extreme Admin Dashboard Control
*   **100% Dynamic Admin Panel:** The admin must have total CRUD (Create, Read, Update, Delete) access to every single feature mentioned above. Real-time visual dashboard showing graphs of sales and low-stock warnings.

---

### 4. 💡 Real-Life Professional Developer Best Practices
*   **Security First:** Implement strict PDO or MySQLi prepared statements. Use CSRF tokens on all forms. Hash all passwords securely (`password_hash()`).
*   **Speed Optimization:** Because we are using 3D assets, ensure they are lazy-loaded via JavaScript.
*   **SEO Best Practices:** Ensure the dynamic PHP files generate proper schema.org markup, semantic HTML5, and clean routing URLs.

### 5. 🏗️ Instructions for Output Generation
Due to the massive scope of this e-commerce project, provide the architecture in logical phases:

1.  **Phase 1:** Provide the complete MySQL database schema (`CREATE TABLE` statements) mapping every feature described above. Make sure the tables are perfectly normalized with Foreign Keys.
2.  **Phase 2:** Show the exact advanced PHP backend MVC folder structure and write the ultra-secure PDO database connection file (`db.php`).
3.  **Phase 3:** Provide the HTML/TailwindCSS layout for the elite Admin Dashboard, applying the light theme and typography setup.
4.  **Phase 4:** Write the HTML/JS for the storefront landing page. Explicitly provide the functional Javascript code needed to include an impressive 3D background animation and the AJAX jQuery logic for seamlessly interacting with the Cart.
5.  **Phase 5:** Provide the PHP Controller logic tracking cart additions, verifying variants, checking inventory levels, and securing the checkout process.

*Confirm you fully understand the exhaustive nature of this PHP custom rebuild and begin with Phase 1.*
