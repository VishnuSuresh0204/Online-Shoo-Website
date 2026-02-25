from django.db import models
from django.contrib.auth.models import AbstractUser

class Login(AbstractUser):
    usertype = models.CharField(max_length=50)
    viewpassword = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    logid = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class SellerProfile(models.Model):
    logid = models.ForeignKey(Login, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.TextField()
    status = models.BooleanField(default=False) 

    def __str__(self):
        return self.shop_name

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class Shoe(models.Model):
    seller = models.ForeignKey(Login, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    size = models.IntegerField()
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='shoe_images/')

    def __str__(self):
        return f"{self.product_name} - ₹{self.price}"

class Cart(models.Model):
    logid = models.ForeignKey(Login, on_delete=models.CASCADE)
    product = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Order(models.Model):
    logid = models.ForeignKey(Login, on_delete=models.CASCADE)
    product = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending")
    delivery_address = models.TextField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Order {self.id} by {self.logid.username}"

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50, default="Pending")
    payment_date = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    logid = models.ForeignKey(Login, on_delete=models.CASCADE)
    product = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    logid = models.ForeignKey(Login, on_delete=models.CASCADE)
    product = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.logid.username}"

class Complaint(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='complainer')
    seller = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='reported_seller')
    subject = models.CharField(max_length=200)
    complaint = models.TextField()
    date = models.DateField(auto_now_add=True)
    reply = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Complaint by {self.user.username} against {self.seller.username}"
