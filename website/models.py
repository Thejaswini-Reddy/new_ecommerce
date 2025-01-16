from django.db import models


# Category model to classify products
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Unique category name
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return self.name  # Display category name in admin panel


# Product model representing items in the store
class Product(models.Model):
    name = models.CharField(max_length=255)  # Product name
    description = models.TextField()  # Product description
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Product price
    stock = models.IntegerField()  # Number of items in stock
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Link to category
    image = models.ImageField(upload_to='product_images/', default='default_image.jpg')  # Product image

    def __str__(self):
        return self.name  # Display product name in admin panel


# Cart model to hold cart details
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp

    def __str__(self):
        return f"Cart {self.id}"  # Display cart ID

    def get_total_price(self):
        """Calculate total price of all items in the cart."""
        return sum(item.get_total_price() for item in self.cartitem_set.all())


# CartItem model representing products added to the cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  # Link to cart
    product = models.ForeignKey('website.Product', on_delete=models.CASCADE)  # Link to product
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"  # Display item details

    def get_total_price(self):
        """Calculate total price for this cart item."""
        return self.product.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)  # Link to Cart
    customer_name = models.CharField(max_length=255)  # Customer name
    customer_email = models.EmailField()  # Customer email
    shipping_address = models.TextField()  # Address for shipping
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')  # Order status
    created_at = models.DateTimeField(auto_now_add=True)  # Date the order was placed
    updated_at = models.DateTimeField(auto_now=True)  # Date the order was last updated

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.orderitem_set.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Link to Order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to Product
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
