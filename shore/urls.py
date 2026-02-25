"""
URL configuration for shore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),
    path("user_reg/", views.user_register),
    path("seller_reg/", views.seller_register),
    path("login/", views.login_view),
    path("logout/", views.logout_view),

    path("user_home/", views.user_home),
    path("seller_home/", views.seller_home),
    path("admin_home/", views.admin_home),
    path("admin_view_users/", views.admin_view_users),
    path("admin_view_sellers/", views.admin_view_sellers),
    path("approve_seller/", views.approve_seller),
    path("reject_seller/", views.reject_seller),
    path("admin_view_products/", views.admin_view_products),
    path("admin_add_category/", views.admin_add_category),
    path("admin_view_category/", views.admin_view_category),
    path("admin_edit_category/", views.admin_edit_category),
    path("admin_view_feedback/", views.admin_view_feedback),
    path("admin_view_all_orders/", views.admin_view_all_orders),

    # User
    path("view_product/", views.view_product),
    path("product_details/", views.product_details),
    path("add_to_cart/", views.add_to_cart),
    path("view_cart/", views.view_cart),
    path("remove_from_cart/", views.remove_from_cart),
    path("update_cart_quantity/", views.update_cart_quantity),
    path("add_to_wishlist/", views.add_to_wishlist),
    path("view_wishlist/", views.view_wishlist),
    path("remove_from_wishlist/", views.remove_from_wishlist),
    path("payment/", views.user_payment),
    path("card_payment/", views.card_payment),
    path("process_card_payment/", views.process_card_payment),
    path("view_orders/", views.user_orders),
    path("add_feedback/", views.user_add_feedback),
    path("edit_feedback/", views.edit_feedback),
    path("delete_feedback/", views.delete_feedback),
    path("my_reviews/", views.user_view_feedback),

    # Seller
    path("seller_add_product/", views.seller_add_product),

    path("seller_view_products/", views.seller_view_products),
    path("seller_edit_product/", views.seller_edit_product),
    path("seller_delete_product/", views.seller_delete_product),
    path("seller_view_orders/", views.seller_view_orders),
    path("update_order_status/", views.seller_update_order_status),
    path("seller_view_feedback/", views.seller_view_feedback),

    # Complaints & Blocking
    path("report_seller/", views.report_seller),
    path("admin_view_complaints/", views.admin_view_complaints),
    path("block_seller/", views.block_seller),
    path("unblock_seller/", views.unblock_seller),
    path("block_user/", views.block_user),
    path("unblock_user/", views.unblock_user),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
