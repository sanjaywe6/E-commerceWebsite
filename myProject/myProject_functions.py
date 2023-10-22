from testingApp.models import *
import re

# function which verfies captcha code when any form is submitted
def verify_captcha(val,id):
    get_captcha = captchaCpde.objects.filter(sno = id).first()
    if get_captcha.value == val:
        return True
    else:
        return False

# function to check whether username is valid  
def is_username_valid(username):
    # checking length
    if len(username)<5:
        return False
    
    # check for special charecter
    if re.search(r'[!@#$%^&*()_{}":;<>,.?~\|]', username):
        return False
    return True

# function for password verification
def is_passwd_valid(passwd):
    # checking password length
    if len(passwd)<8:
        return False
    
    # checking for special charecter existence
    if not re.search(r'[!@#$%^&*()_{}":;<>,.?~\|]',passwd):
        return False

    # checking atleast one uppercase letter
    if not any(val.isupper() for val in passwd):
        return False
    
    # checking atleast one lowercase letter
    if not any(val.islower() for val in passwd):
        return False
    
    # checking for atleast one digit
    if not any(val.isdigit() for val in passwd):
        return False
    
    return True

def verify_user_registration_form(fname, lname, username, email, passwd, passwdc):
    status = {}
    if len(fname)>0:
        if len(lname)>0:
            if is_username_valid(username) == True:
                if len(email)>0:
                    if is_passwd_valid(passwd) == True:
                        if passwd == passwdc:
                            status['verification'] = True
                            status['msg'] = ''
                        else:
                            status['verification'] = False
                            status['msg'] = 'Sorry!, Passwords did not match..'
                    else:
                        status['verification'] = False
                        status['msg'] = 'Sorry!, Password was invalid..'
                else:
                    status['verification'] = False
                    status['msg'] = 'Sorry!, Email field was empty..'
            else:
                status['verification'] = False
                status['msg'] = 'Sorry!, Username is not valid..'
        else:
            status['verification'] = False
            status['msg'] = 'Sorry!, Last Name field was empty..'
    else:
        status['verification'] = False
        status['msg'] = 'Sorry!, First Name field was empty..'
    return status

# function for updating cart
def updateCart(request,id,operation):

    # adding item to cart
    if operation == 'add':

        # getting particular cart data saved with logged in user
        get_cart = productsCart.objects.filter(usrname = request.user).first()

        # if cart is empty for that user
        if get_cart == None:

            # generating a dictionary
            cart_dict = {
                id:1,
            }
            try:
                # saving to cart database
                cart_db = productsCart(usrname = request.user, prod_ids = cart_dict)
                cart_db.save()
            except Exception:
                return False

        else:
            # targetting product id dictionary saved in cart
            db_dict = get_cart.prod_ids

            # if given id alredy in cart
            if id in db_dict:
                # incrementing quantity of product in cart with given id
                db_dict[id]+=1
                try:
                    # saving to database
                    get_cart.prod_ids = db_dict
                    get_cart.save()
                except Exception:
                    return False

            else:
                # adding new key value in dictionary
                db_dict[id]=1
                try:
                    # saving to database
                    get_cart.prod_ids = db_dict
                    get_cart.save()
                except Exception:
                    return False
    # removing item from cart
    elif operation == 'remove':
        # getting particular cart data saved with logged in user
        get_cart = productsCart.objects.filter(usrname = request.user).first()

        # if cart is empty for that user
        if get_cart == None:
            return False
        
        else:
            # targetting product id dictionary saved in cart
            db_dict = get_cart.prod_ids
            
            # remove id from cart dictionary
            del db_dict[id]
            
            try:
                # saving to database
                get_cart.prod_ids = db_dict
                get_cart.save()
            except Exception:
                return False

    return True

# function for verifying comment
def verify_comment(request, product_id, comment):

    if re.search(r'[!#$%^&*:;<>~\|]',comment):
        return False
    if len(comment)<1:
        return False
    return True