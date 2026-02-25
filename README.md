# Online Shoo Website (Karma Shop)

A modern, premium e-commerce platform built with Django for buying and selling shoes.

## 🚀 Features

### For Customers
- **Product Discovery**: Browse shoes with advanced category filtering and search.
- **Product Details**: Comprehensive view with images, specifications, and seller information.
- **Cart & Wishlist**: Manage items you want to buy or save for later.
- **Integrated Feedback System**: 
    - Rate products with a star system.
    - Write, Edit, and Delete your own reviews.
    - Restrictions: Only customers who have purchased a product can leave a review (1 review per product).
- **Order Management**: Track orders with a premium dashboard and status-aware badges.
- **My Reviews Dashboard**: Manage all your submitted feedback in one place.
- **Secure Checkout**: Integrated payment simulation.

### For Sellers
- **Product Management**: Add and manage shoe listings with size and color variants.
- **Order Tracking**: View and process customer orders.

### For Administrators
- **User Management**: Approve/Decline seller registrations.
- **Content Moderation**: Monitor customer feedback and complaints.

## 🛠️ Tech Stack
- **Backend**: Python, Django 5.x
- **Frontend**: HTML5, Vanilla CSS, JavaScript, Bootstrap
- **Database**: SQLite3
- **Icons**: Linearicons, Themify Icons, Font Awesome

## 💻 Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/VishnuSuresh0204/Online-Shoo-Website.git
   cd Online-Shoo-Website
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install django
   ```

4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   Open `http://127.0.0.1:8000` in your browser.

---
*Created by [Vishnu Suresh](https://github.com/VishnuSuresh0204)*
