from django.shortcuts import render, redirect
from django.http import JsonResponse
from testingApp.models import *
from . import myProject_functions
import random
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import  logout
from django.contrib.auth import  authenticate
from django.contrib.auth.models import User

def home(request):
    student_laptop = allProducts.objects.filter(category = 'Student')
    business_laptop = allProducts.objects.filter(category = 'Business')
    gaming_laptop = allProducts.objects.filter(category = 'Gaming')
    param = {'student_laptop':student_laptop,'business_laptop':business_laptop, 'gaming_laptop':gaming_laptop}
    return render(request, 'home.html', param)
# function for signup page
def signup(request):
    # getting form data in post request
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        usrname = request.POST.get('inputUsername')
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')
        passwdc = request.POST.get('passwdc')

        # getting captcha vlaues
        captcha_val = request.POST.get('captcha_value')
        captcha_id = request.POST.get('captcha_id')

        # verifying captcha
        if myProject_functions.verify_captcha(captcha_val, captcha_id) == True:

            # verifying form
            verify_form = myProject_functions.verify_user_registration_form(fname, lname, usrname, email, passwd, passwdc)

            if verify_form['verification'] == True:

                # create user with received username and password
                User.objects.create_user(username=usrname, password=passwd)

                # verifying whether user is logedin with given username or not after registration
                user = authenticate(username=usrname, password=passwd)
                if user != None:
                    try:
                        # creating login session
                        login(request,user)
                        return redirect('/')
                    except Exception as e:
                        messages.add_message(request,40,"Unknown error found. Please contact to admin...")
            else:
                messages.add_message(request,40,f"{verify_form['msg']}")

        else:
            messages.add_message(request,40,'Sorry!, Captcha verification failed')
    captcha = random.choice(captchaCpde.objects.all())
    param = {'captcha':captcha}
    return render(request, 'signup.html', param)

def loginUser(request):
    # getting form data in post request
    if request.method == 'POST':
        usrname = request.POST.get('inputUsername')
        passwd = request.POST.get('passwd')

        # getting captcha vlaues
        captcha_val = request.POST.get('captcha_value')
        captcha_id = request.POST.get('captcha_id')

        # verifying captcha
        if myProject_functions.verify_captcha(captcha_val, captcha_id) == True:
            user = authenticate(request, username=usrname, password=passwd)
            if user is not None:
                try:
                    login(request, user)
                    return redirect('/')
                except Exception as e:
                    messages.add_message(request,40,'Sorry!, Unknown error found. Please contact to admin...') 
            else:
                messages.add_message(request,40,'Sorry!, Wrong user credentials...') 
        else:
            messages.add_message(request,40,'Sorry!, Captcha verification failed...')

    captcha = random.choice(captchaCpde.objects.all())
    param = {'captcha':captcha}
    return render(request, 'login.html', param)

# function for logging out the user
def logoutUser(request):
    logout(request)
    return redirect('/')

# fuction to return particular product filtered with id
def product_with_id(request,id):
    # filter product with id
    get_product = allProducts.objects.filter(id=id).first()

    # getting other same products from allProducts model
    same_products = allProducts.objects.filter(category = get_product.category)

    # getting saved comments on that product
    # get_comment = productComment.objects.filter(product_id = id).order_by('-time')

    param = {'product':get_product,'same_products':same_products}
    return render(request, 'product_with_id.html', param)

# function fpr working with cart
def update_cart(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        operation = request.GET.get('operation')

        # running update cart function and returning True or Flase as per status of operation
        try:
            update_cart = myProject_functions.updateCart(request,id,operation)
        except Exception:
            update_cart = False

        # returning updated cart items
        # var for adding product item and quantity in dict
        cart_products = []
        try:
            get_cart_data = productsCart.objects.filter(usrname = request.user).first()

            # iterating over all added product id in cart item
            for product, quantity in get_cart_data.prod_ids.items():

                # getting product with given id
                get_product_with_id = allProducts.objects.filter(id = product).values().first()
                # adding product as key and quantity as value in dict
                data = {
                    'product':get_product_with_id,
                    'quantity':quantity,
                }
                cart_products.append(data)
        except Exception:
            pass

        return JsonResponse({'status':update_cart,'cart_products':cart_products})

# function fpr working with cart
def cart(request):
    # accessing cart procut with for login user
    try:
        get_cart_data = productsCart.objects.filter(usrname = request.user).first()
        # if cart item is none
        if get_cart_data == None:
            cart_products = {}
        # if item in cart found
        else:
            # var for adding product item and quantity in dict
            cart_products = dict()
            # iterating over all added product id in cart item
            for item, val in get_cart_data.prod_ids.items():
                # getting product with given id
                get_product_with_id = allProducts.objects.filter(id = item).first()
                # adding product as key and quantity as value in dict
                cart_products[get_product_with_id] = val
    except Exception:
        cart_products = {}

    # making list to send data on page
    cart_products = [(key, val) for key, val in cart_products.items()]
    param = {'cart_products':cart_products}
    return render(request, 'cart.html', param)

# function for returning all products with same category
def product_with_category(request,category):
    get_products = allProducts.objects.filter(category = category)
    param = {'products':get_products}
    return render(request,'product_with_category.html', param)

# # function for adding comment
def comment(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        comment = request.POST.get('comment')
        # verifying comment
        if myProject_functions.verify_comment(request,product_id,comment) == True:

            # saving to database
            get_comment = productComment(usr = request.user,usrname= request.user.username, product_id=product_id, comment=comment)
            get_comment.save()

            # getting saall saved comment for that product
            load_comment = productComment.objects.filter(product_id = product_id).values().order_by('-time')
            load_comment = list(load_comment)

            return JsonResponse({'status':True,'msg':'Great!, your comment has been saved...','comments':load_comment})
        else:
            return JsonResponse({'status':False, 'msg':'Sorry!, Please check your comment. Special charecters or blank comment are not allowed...'})