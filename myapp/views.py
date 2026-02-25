from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .models import *


# -------------------- COMMON --------------------

def index(request):
    return render(request, "index.html")


# -------------------- USER --------------------

def user_register(request):
    if request.method == "POST":
        
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        password = request.POST.get("password")

        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
            return redirect("/user_reg")

        user = Login.objects.create_user(
            username=email,
            password=password,
            usertype="user",
            viewpassword=password
        )

        UserProfile.objects.create(
            logid=user,
            name=name,
            email=email,
            phone=phone,
            address=address
        )

        messages.success(request, "User registered successfully")
        return redirect("/login")

        

    return render(request, "user_register.html")


def user_home(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        return render(request, "USER/index.html")
    return redirect("/login")


def view_product(request):
    if request.user.is_authenticated and request.user.usertype == "user":

        products = Shoe.objects.all()
        categories = Category.objects.all()

        # ---- SEARCH ----
        search = request.GET.get("search")
        

        # ---- FILTER BY CATEGORY ----
        category_id = request.GET.get("category")
        if category_id:
            products = products.filter(category_id=category_id)

        # ---- FILTER BY SIZE ----
        size = request.GET.get("size")
        if size:
            products = products.filter(size=size)

        # ---- FILTER BY PRICE ----
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")

        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        # Get user's cart and wishlist product IDs
        cart_ids = set(Cart.objects.filter(logid=request.user).values_list('product_id', flat=True))
        wishlist_ids = set(Wishlist.objects.filter(logid=request.user).values_list('product_id', flat=True))

        product_list = []

        for product in products:
            seller = SellerProfile.objects.filter(
                logid=product.seller,
                status=True
            ).first()

            if seller:
                product_list.append({
                    "product": product,
                    "seller": seller,
                    "in_cart": product.id in cart_ids,
                    "in_wishlist": product.id in wishlist_ids
                })


        return render(request, "USER/view_product.html", {
            "product_list": product_list,
            "categories": categories
        })

    return redirect("/login")


def add_to_cart(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        pid = request.GET.get("pid")
        product = Shoe.objects.get(id=pid)
        cart_item = Cart.objects.filter(
            logid=request.user,
            product=product
        ).first()

        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
        else:
            Cart.objects.create(
                logid=request.user,
                product=product,
                quantity=1
            )
        messages.success(request, "Added to cart")
        return redirect("/view_product")
    return redirect("/login")


def view_cart(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        cart_items = Cart.objects.filter(logid=request.user)
        total_price = 0
        for item in cart_items:
            total_price += item.product.price * item.quantity

        return render(request, "USER/cart.html", {
            "cart_items": cart_items,
            "total_price": total_price
        })
    return redirect("/login")


def remove_from_cart(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        cid = request.GET.get("cid")
        Cart.objects.filter(id=cid).delete()
        return redirect("/view_cart")
    return redirect("/login")


def update_cart_quantity(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        cid = request.GET.get("cid")
        action = request.GET.get("action")
        cart_item = Cart.objects.filter(id=cid).first()

        if cart_item:
            if action == "increase":
                cart_item.quantity += 1
                cart_item.save()
            elif action == "decrease":
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    # Optional: Remove if quantity is 1? 
                    # For now just strictly stay at 1. User can use remove button.
                    pass
        
        return redirect("/view_cart")
    return redirect("/login")


def add_to_wishlist(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        pid = request.GET.get("pid")
        product = Shoe.objects.get(id=pid)
        if not Wishlist.objects.filter(logid=request.user, product=product).exists():
            Wishlist.objects.create(
                logid=request.user,
                product=product
            )
            messages.success(request, "Added to wishlist")
        else:
            messages.info(request, "Already in wishlist")
        return redirect("/view_product")
    return redirect("/login")


def view_wishlist(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        wishlist_items = Wishlist.objects.filter(logid=request.user)
        return render(request, "USER/wishlist.html", {"wishlist_items": wishlist_items})
    return redirect("/login")


def remove_from_wishlist(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        wid = request.GET.get("wid")
        Wishlist.objects.filter(id=wid).delete()
        return redirect("/view_wishlist")
    return redirect("/login")


def user_payment(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        if request.method == "POST":
            # Process payment (mock)
            cart_items = Cart.objects.filter(logid=request.user)
            address = request.POST.get("address")
            phone = request.POST.get("phone")
            payment_method = request.POST.get("payment_method")

            if not cart_items:
                messages.error(request, "Cart is empty")
                return redirect("/user_home")

            if payment_method == "MockCard":
                # Store details in session and redirect to card payment page
                request.session['payment_address'] = address
                request.session['payment_phone'] = phone
                return redirect("/card_payment")

            for item in cart_items:
                order = Order.objects.create(
                    logid=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    status="Pending",
                    delivery_address=address,
                    contact_number=phone
                )
                Payment.objects.create(
                    order=order,
                    payment_method=payment_method,
                    payment_status="Paid"
                )
                # Reduce product quantity
                item.product.quantity -= item.quantity
                item.product.save()

            # Clear cart
            cart_items.delete()
            messages.success(request, "Order placed successfully")
            return redirect("/view_orders")

        # GET request: Show payment page with total, pre-filled with user data
        cart_items = Cart.objects.filter(logid=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        
        # Fetch user profile for pre-filling
        user_profile = UserProfile.objects.filter(logid=request.user).first()
        
        return render(request, "USER/payment.html", {
            "total_price": total_price,
            "user_profile": user_profile
        })
    return redirect("/login")


def card_payment(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        # Get total price again (or pass via session, but recalculating is safer)
        cart_items = Cart.objects.filter(logid=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        if not cart_items:
             return redirect("/user_home")
        
        return render(request, "USER/card_payment.html", {"total_price": total_price})
    return redirect("/login")


def process_card_payment(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        if request.method == "POST":
            # Retrieving stored details
            address = request.session.get('payment_address')
            phone = request.session.get('payment_phone')
            
            # Here you would typically validate card details from request.POST
            # card_number = request.POST.get("card_number") ...

            cart_items = Cart.objects.filter(logid=request.user)
            if not cart_items:
                return redirect("/user_home")

            for item in cart_items:
                order = Order.objects.create(
                    logid=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    status="Pending",
                    delivery_address=address,
                    contact_number=phone
                )
                Payment.objects.create(
                    order=order,
                    payment_method="Card",
                    payment_status="Paid"
                )
                item.product.quantity -= item.quantity
                item.product.save()

            cart_items.delete()
            
            # Clear session data
            if 'payment_address' in request.session: del request.session['payment_address']
            if 'payment_phone' in request.session: del request.session['payment_phone']
            
            messages.success(request, "Order placed successfully")
            return redirect("/view_orders")
    return redirect("/login")


def user_orders(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        orders = Order.objects.filter(logid=request.user).order_by("-order_date")
        
        # Add review status for each order
        order_list = []
        for order in orders:
            has_reviewed = Review.objects.filter(
                logid=request.user, 
                product=order.product
            ).exists()
            order_list.append({
                "order": order,
                "has_reviewed": has_reviewed
            })
            
        return render(request, "USER/uorders.html", {"order_list": order_list})
    return redirect("/login")


def product_details(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        pid = request.GET.get("pid")
        product = Shoe.objects.filter(id=pid).first()
        if not product:
            messages.error(request, "Product not found")
            return redirect("/view_product/")
        seller = SellerProfile.objects.filter(logid=product.seller, status=True).first()
        reviews = Review.objects.filter(product=product).order_by("-date")
        cart_ids = set(Cart.objects.filter(logid=request.user).values_list('product_id', flat=True))
        wishlist_ids = set(Wishlist.objects.filter(logid=request.user).values_list('product_id', flat=True))
        avg_rating = 0
        if reviews:
            avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1)
        user_review = Review.objects.filter(logid=request.user, product=product).first()
        has_ordered = Order.objects.filter(logid=request.user, product=product).exists()
        return render(request, "USER/product_details.html", {
            "product": product,
            "seller": seller,
            "reviews": reviews,
            "avg_rating": avg_rating,
            "in_cart": product.id in cart_ids,
            "in_wishlist": product.id in wishlist_ids,
            "user_review": user_review,
            "has_ordered": has_ordered,
        })
    return redirect("/login")


def user_add_feedback(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        pid = request.GET.get("pid")
        product = Shoe.objects.filter(id=pid).first()
        if not product:
            messages.error(request, "Product not found")
            return redirect("/view_product/")

        # Check if user has ordered this product
        has_ordered = Order.objects.filter(logid=request.user, product_id=pid).exists()
        if not has_ordered:
            messages.error(request, "You can only review products you have ordered.")
            return redirect("/product_details/?pid=" + str(pid))

        # Check if user has already reviewed this product
        existing_review = Review.objects.filter(logid=request.user, product_id=pid).first()
        if existing_review:
            messages.error(request, "You have already submitted a review for this product.")
            return redirect("/product_details/?pid=" + str(pid))

        if request.method == "POST":
            rating = request.POST.get("rating")
            comment = request.POST.get("comment")
            Review.objects.create(
                logid=request.user,
                product_id=pid,
                rating=rating,
                comment=comment
            )
            messages.success(request, "Review submitted successfully!")
            return redirect("/product_details/?pid=" + str(pid))

        return render(request, "USER/add_feedback.html", {"product": product})
    return redirect("/login")


def edit_feedback(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        rid = request.GET.get("rid")
        review = Review.objects.filter(id=rid, logid=request.user).first()
        if not review:
            messages.error(request, "Review not found or access denied.")
            return redirect("/view_orders/")
        if request.method == "POST":
            review.rating = request.POST.get("rating")
            review.comment = request.POST.get("comment")
            review.save()
            messages.success(request, "Review updated successfully!")
            return redirect("/product_details/?pid=" + str(review.product_id))
        return render(request, "USER/edit_feedback.html", {"review": review, "product": review.product})
    return redirect("/login")


def delete_feedback(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        rid = request.GET.get("rid")
        review = Review.objects.filter(id=rid, logid=request.user).first()
        if review:
            pid = review.product_id
            review.delete()
            messages.success(request, "Review deleted.")
            return redirect("/product_details/?pid=" + str(pid))
        messages.error(request, "Review not found.")
        return redirect("/view_orders/")
    return redirect("/login")



def user_view_feedback(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        reviews = Review.objects.filter(logid=request.user).order_by("-date")
        return render(request, "USER/my_reviews.html", {"reviews": reviews})
    return redirect("/login")


# -------------------- SELLER --------------------

def seller_register(request):
    if request.method == "POST":
        shop_name = request.POST.get("shop_name")
        owner_name = request.POST.get("owner_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        password = request.POST.get("password")

        if Login.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
            return redirect("/seller_reg")

        seller_login = Login.objects.create_user(
            username=email,
            password=password,
            usertype="seller",
            viewpassword=password
        )

        SellerProfile.objects.create(
            logid=seller_login,
            shop_name=shop_name,
            owner_name=owner_name,
            phone=phone,
            address=address,
            status=False
        )

        messages.success(request, "Seller registered. Wait for admin approval.")
        return redirect("/login")

    return render(request, "seller_register.html")


def seller_home(request):
    if request.user.is_authenticated and request.user.usertype == "seller":
        seller = SellerProfile.objects.filter(
            logid=request.user,
            status=True
        ).first()
        if seller:
            return render(request, "SELLER/index.html")
    return redirect("/login")


def seller_add_product(request):
    if request.user.is_authenticated and request.user.usertype == "seller":
        seller = SellerProfile.objects.filter(
            logid=request.user,
            status=True
        ).first()

        if seller:
            categories = Category.objects.all()

            if request.method == "POST":
                Shoe.objects.create(
                    seller=request.user,
                    product_name=request.POST.get("product_name"),
                    category_id=request.POST.get("category"),
                    brand=request.POST.get("brand"),
                    size=request.POST.get("size"),
                    color=request.POST.get("color"),
                    price=request.POST.get("price"),
                    quantity=request.POST.get("quantity"),
                    description=request.POST.get("description"),
                    image=request.FILES.get("image")
                )
                messages.success(request, "Product added successfully")
                return redirect("/seller_view_products")

            return render(request, "SELLER/add_product.html", {"categories": categories})

    return redirect("/login")

    




def seller_view_products(request):
    if request.user.is_authenticated and request.user.usertype == "seller":
        products = Shoe.objects.filter(seller=request.user)
        categories = Category.objects.all()

        # ---- FILTER BY CATEGORY ----
        category_id = request.GET.get("category")
        if category_id:
            products = products.filter(category_id=category_id)

        return render(request, "SELLER/view_products.html", {
            "products": products,
            "categories": categories
        })
    return redirect("/login")


def seller_delete_product(request):
    if request.user.is_authenticated and request.user.usertype == "seller":
        pid = request.GET.get("pid")
        product = Shoe.objects.filter(
            id=pid,
            seller=request.user
        ).first()

        if product:
            product.delete()
            messages.success(request, "Product deleted successfully")
        else:
            messages.error(request, "Product not found or unauthorized")
        
        return redirect("/seller_view_products")
    return redirect("/login")


def seller_edit_product(request):
    if request.user.is_authenticated and request.user.usertype == "seller":
        pid = request.GET.get("pid")
        product = Shoe.objects.filter(
            id=pid,
            seller=request.user
        ).first()

        if product:
            categories = Category.objects.all()

            if request.method == "POST":
                product.product_name = request.POST.get("product_name")
                product.brand = request.POST.get("brand")
                product.size = request.POST.get("size")
                product.color = request.POST.get("color")
                product.price = request.POST.get("price")
                product.quantity = request.POST.get("quantity")
                product.description = request.POST.get("description")
                product.category_id = request.POST.get("category")

                if request.FILES.get("image"):
                    product.image = request.FILES.get("image")

                product.save()
                messages.success(request, "Product updated successfully")
                return redirect("/seller_view_products")

            return render(request, "SELLER/edit_product.html", {
                "product": product,
                "categories": categories
            })

    return redirect("/login")


def seller_view_orders(request):
    if request.user.is_authenticated and request.user.usertype == "seller":
        orders = Order.objects.filter(
            product__seller=request.user
        )

        sort_by = request.GET.get("sort")
        if sort_by == "oldest":
            orders = orders.order_by("order_date")
        else:
            orders = orders.order_by("-order_date")

        return render(request, "SELLER/view_orders.html", {"orders": orders})

    return redirect("/login")


def seller_update_order_status(request):
    if request.user.is_authenticated and request.user.usertype == "seller":
        oid = request.GET.get("oid")
        order = Order.objects.filter(
            id=oid,
            product__seller=request.user
        ).first()

        if order and request.method == "POST":
            new_status = request.POST.get("status")

            valid_flow = {
                "Pending": ["Confirmed"],
                "Confirmed": ["Shipped"],
                "Shipped": ["Delivered"]
            }

            if new_status in valid_flow.get(order.status, []):
                order.status = new_status
                order.save()
                messages.success(request, "Order status updated")
            else:
                messages.error(request, "Invalid status change")

        return redirect("/seller_view_orders")

    return redirect("/login")


def seller_view_feedback(request):
    if request.user.is_authenticated and request.user.usertype == "seller":
        # Reviews for products owned by this seller
        reviews = Review.objects.filter(product__seller=request.user)
        return render(request, "SELLER/view_feedback.html", {"reviews": reviews})
    return redirect("/login")


# -------------------- LOGIN / LOGOUT --------------------

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:

            # 🔒 SELLER APPROVAL CHECK
            if user.usertype == "seller":
                seller = SellerProfile.objects.filter(logid=user).first()

                if seller is None:
                    messages.error(request, "Seller profile not found")
                    return redirect("/login")

                if seller.status == False:
                    messages.error(
                        request,
                        "Your account is waiting for admin approval"
                    )
                    return redirect("/login")

            # ✅ LOGIN ALLOWED
            auth_login(request, user)
            request.session["usertype"] = user.usertype

            if user.usertype == "admin":
                return redirect("/admin_home")

            elif user.usertype == "user":
                user_profile = UserProfile.objects.filter(logid=user).first()
                if user_profile and user_profile.status == False:
                    messages.error(request, "Your account is blocked by admin")
                    return redirect("/login")
                request.session["user_id"] = user.id
                return redirect("/user_home")

            elif user.usertype == "seller":
                seller = SellerProfile.objects.filter(logid=user).first() # Fetch seller again or move logic up
                request.session["seller_id"] = seller.id
                return redirect("/seller_home")

        else:
            messages.error(request, "Invalid username or password")
            return redirect("/login")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("/index")

# -------------------- ADMIN --------------------

def admin_home(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        return render(request, "ADMIN/index.html")
    return redirect("/login")


def admin_view_users(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        user_logins = Login.objects.filter(usertype="user")
        users_data = []
        for u in user_logins:
            profile = UserProfile.objects.filter(logid=u).first()
            users_data.append({
                "login": u,
                "profile": profile
            })
        return render(request, "ADMIN/admin_view_users.html", {
            "users_data": users_data
        })
    return redirect("/login")


def admin_view_sellers(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        return render(request, "ADMIN/admin_view_all_sellers.html", {
            "sellers": SellerProfile.objects.all()
        })
    return redirect("/login")


def approve_seller(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        sid = request.GET.get("sid")
        seller = SellerProfile.objects.filter(id=sid).first()
        if seller:
            seller.status = True
            seller.save()
        return redirect("/admin_view_sellers")
    return redirect("/login")


def admin_view_products(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        products = Shoe.objects.all()
        product_list = []
        for product in products:
            seller = SellerProfile.objects.filter(logid=product.seller).first()
            if seller:
                product_list.append({
                    "product": product,
                    "seller": seller
                })
        return render(request, "ADMIN/admin_view_products.html", {"product_list": product_list})
    return redirect("/login")


def admin_add_category(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        if request.method == "POST":
            name = request.POST.get("category_name")
            if not Category.objects.filter(category_name=name).exists():
                Category.objects.create(category_name=name)
        return render(request, "ADMIN/add_category.html")
    return redirect("/login")


def admin_view_category(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        return render(request, "ADMIN/view_category.html", {
            "categories": Category.objects.all()
        })
    return redirect("/login")


def admin_edit_category(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        cid = request.GET.get("cid")
        category = Category.objects.filter(id=cid).first()
        if category and request.method == "POST":
            category.category_name = request.POST.get("category_name")
            category.save()
        return render(request, "ADMIN/edit_category.html", {"category": category})
    return redirect("/login")


def admin_view_feedback(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        reviews = Review.objects.all()
        feedback_list = []
        for review in reviews:
            product = review.product
            seller = SellerProfile.objects.filter(logid=product.seller).first()
            user = UserProfile.objects.filter(logid=review.logid).first()
            
            if seller and user:
                feedback_list.append({
                    "review": review,
                    "product": product,
                    "seller": seller,
                    "user": user
                })

        return render(request, "ADMIN/admin_view_feedback.html", {
            "feedback_list": feedback_list
        })
    return redirect("/login")


def admin_view_all_orders(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        orders = Order.objects.all()

        sort_by = request.GET.get("sort")
        if sort_by == "oldest":
            orders = orders.order_by("order_date")
        else:
            orders = orders.order_by("-order_date")

        return render(request, "ADMIN/view_orders.html", {"orders": orders})
    return redirect("/login")


def reject_seller(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        sid = request.GET.get("sid")
        seller = SellerProfile.objects.filter(id=sid).first()
        if seller:
            seller.delete() # Or set status to specific 'Rejected' state if needed, but delete is cleaner for "Reject"
            # Also delete the Login user? Maybe not, they might want to register as user. 
            # But usually reject implies removing the seller request. 
            # For now, let's just delete the profile.
            messages.success(request, "Seller rejected")
        return redirect("/admin_view_sellers")
    return redirect("/login")

# -------------------- COMPLAINTS & BLOCKING --------------------

def report_seller(request):
    if request.user.is_authenticated and request.user.usertype == "user":
        sid = request.GET.get("sid")
        reported_seller_user = Login.objects.get(id=sid)
        
        if request.method == "POST":
            subject = request.POST.get("subject")
            complaint_text = request.POST.get("complaint")
            
            Complaint.objects.create(
                user=request.user,
                seller=reported_seller_user,
                subject=subject,
                complaint=complaint_text
            )
            messages.success(request, "Complaint submitted successfully")
            return redirect("/user_home") 

        return render(request, "USER/add_complaint.html", {"seller": reported_seller_user})
    return redirect("/login")


def admin_view_complaints(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        complaints = Complaint.objects.all().order_by("-date")
        return render(request, "ADMIN/view_complaints.html", {"complaints": complaints})
    return redirect("/login")


def block_seller(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        sid = request.GET.get("sid") 
        seller = SellerProfile.objects.filter(id=sid).first()
        if seller:
            seller.status = False
            seller.save()
            messages.success(request, "Seller has been blocked")
        return redirect("/admin_view_sellers")
    return redirect("/login")

def unblock_seller(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        sid = request.GET.get("sid")
        seller = SellerProfile.objects.filter(id=sid).first()
        if seller:
            seller.status = True
            seller.save()
            messages.success(request, "Seller has been unblocked")
        return redirect("/admin_view_sellers")
    return redirect("/login")


def block_user(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        uid = request.GET.get("uid")
        user_profile = UserProfile.objects.filter(logid_id=uid).first()
        if user_profile:
            user_profile.status = False
            user_profile.save()
            messages.success(request, "User has been blocked")
        return redirect("/admin_view_users")
    return redirect("/login")


def unblock_user(request):
    if request.user.is_authenticated and request.user.usertype == "admin":
        uid = request.GET.get("uid")
        user_profile = UserProfile.objects.filter(logid_id=uid).first()
        if user_profile:
            user_profile.status = True
            user_profile.save()
            messages.success(request, "User has been unblocked")
        return redirect("/admin_view_users")
    return redirect("/login")


