# website/views.py
from django.shortcuts import render, get_object_or_404,redirect
from .models import Product,Cart, CartItem,Category
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'store/register.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'store/login.html', {'form': form})

# View to display all products on the home page
def home(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    category_id = request.GET.get('category', None)  # Get selected category if any
    products = Product.objects.all()  # Get all products from the database
    
    if query:
        products = products.filter(name__icontains=query)  # Search products by name
    
    if category_id:
        products = products.filter(category_id=category_id)  # Filter by category
    
    categories = Category.objects.all()  # To display categories in the filter
    
    return render(request, 'store/home.html', {'products': products, 'categories': categories, 'query': query, 'category_id': category_id})
# View to display details of a single product
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)  # Get product by its ID or show 404 if not found
    return render(request, 'store/product_detail.html', {'product': product})
def add_to_cart(request,id):
    product = get_object_or_404(Product, id=id)
    cart, created = Cart.objects.get_or_create(id=request.session.get('cart_id'))
    request.session['cart_id'] = cart.id  # Store cart ID in the session

    # Check if product already exists in cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')
def cart_detail(request):
    cart = None
    if request.session.get('cart_id'):
        cart = Cart.objects.get(id=request.session['cart_id'])
    return render(request, 'store/cart_detail.html', {'cart': cart})
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart_detail')
def user_logout(request):
    logout(request)
    return redirect('home')
