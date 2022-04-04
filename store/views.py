from django.shortcuts import render, HttpResponse, redirect
from .models import Order, Product, Category, Customer
from django.contrib.auth.hashers import make_password, check_password
from store.middleware.auth import simple_middleware
from django.utils.decorators import method_decorator
from django.views import View


class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('homepage')

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        product = None
        categories = Category.get_all_category
        categoryid = request.GET.get('category')
        if categoryid:
            product = Product.get_all_products_by_categoryid(categoryid)
        else:
            product = Product.get_all_products
        data = {}
        data['product'] = product
        data['categories'] = categories
        print('you are :', request.session.get('email'))
        return render(request, 'index.html', data)


def home(request):
    product = None
    categories = Category.get_all_category
    categoryid = request.GET.get('category')
    if categoryid:
        product = Product.get_all_products_by_categoryid(categoryid)
    else:
        product = Product.get_all_products
    data = {}
    data['product'] = product
    data['categories'] = categories
    print('you are :', request.session.get('email'))
    return render(request, 'index.html', data)


def validation(customer):
    error_message = None
    if(not customer.firstname):
        error_message = 'First Name Requried'
    elif len(customer.firstname) < 4:
        error_message = 'First name must be 4 char long'
    elif not customer.lastname:
        error_message = 'Last Name Requried'

    elif len(customer.lastname) < 4:
        error_message = 'Last name must be 4 char long'
    elif len(customer.email) < 5:
        error_message = 'Email must be 4 char long'
    elif len(customer.password) < 6:
        error_message = 'Password must be 5 char long'
    elif customer.isExists():
        error_message = 'Email Already Exist..'

    return error_message


def register(request):
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')
    password = request.POST.get('password')
    value = {
        'firstname': firstname,
        'lastname': lastname,
        'email': email
    }
    error_message = None
    customer = Customer(firstname=firstname,
                        lastname=lastname, email=email, password=password)
    error_message = validation(customer)
    if not error_message:

        print('firstname', 'lastname', 'email', 'password')
        customer.password = make_password(customer.password)
        customer.save()
        return redirect('login')
    else:
        data = {
            'error': error_message,
            'values': value
        }
        return render(request, 'signup.html', data)


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        return register(request)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            userpassword = Customer.objects.get(email=email)

            request.session['customer'] = userpassword.id
            flag = check_password(password, userpassword.password)
            if flag:
                return redirect('homepage')
            else:
                errormsg = 'Password is Invalid!'
        else:
            errormsg = 'Email is Invalid!'
        print(customer)

        formData = {
            'Email': email,
            'error': errormsg
        }
        return render(request, 'login.html', formData)


def logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)

        return render(request, 'cart.html', {'products': products})


class Checkout(View):
    def post(self, request):
        print(request.POST)
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(location, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            orders = Order(customer=Customer(id=customer),product=product,price=product.price,location=location,phone=phone,quantity=cart.get(str(product.id)))
            orders.save()
        request.session['cart'] = {}

        return redirect('cart')


class OrderView(View):

    @method_decorator(simple_middleware)
    def get(self,request):
        customer=request.session.get('customer')
        orders=Order.get_orders_by_customer(customer)
        print(orders)
        orders=orders.reverse()
        return render(request,'orders.html',{'orders':orders})

def home(request):
    return render(request,'home.html')