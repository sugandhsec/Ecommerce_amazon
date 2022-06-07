from random import randrange

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from app_buyer.models import User,Cart
from app_seller.models import Products

from . import *


# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        try:
            User.objects.get(email = request.POST['email'])
            return render(request, 'register.html',{'msg':'Email is already registered'})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                global temp
                temp = {
                    'fullname': request.POST['fname'],
                    'email': request.POST['email'],
                    'password': request.POST['password'],
                }

                global otp
                otp = randrange(1000,9999)
                subject = 'Welcome to Ecommerce '
                message = f'Thank you for registering and your OTP is {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )

                return render(request, 'otp.html')
            else:
                return render(request, 'register.html',{'msg':'Both passwords is not same'})
    else:
        return render(request, 'register.html')

def otp(request):
    if request.method == 'POST':
        if int(request.POST['otp']) == otp:
            User.objects.create(
                fullname = temp['fullname'],
                email = temp['email'],
                password = temp['password']
            )
            return render(request, 'login.html', {'msg': 'Successfully Registered!!'})
        else:
            return render(request, 'otp.html', {'msg': 'otp wrong!!'})
    else:
        return render(request,'otp.html')

def login(request):
    try:
        request.session['email']
        session_user_data = User.objects.get(email = request.session['email'])
        return render(request,'index.html',{'user_data':session_user_data})
    except:
        if request.method == 'POST':
            try:
                uid = User.objects.get(email = request.POST['email'])
                if request.POST['password'] ==  uid.password:
                    request.session['email'] = request.POST['email']
                    session_user_data = User.objects.get(email = request.session['email'])
                    global order_id
                    cart_obj = Cart.objects.filter(userid = session_user_data)
                    if len(cart_obj) != 0:
                         oid = cart_obj.values()
                         order_id = oid[0]['orderid']
                    else:
                         order_id = randrange(1000,9999)
                    return render(request, 'index.html',{'user_data':session_user_data})
                else:
                    return render(request, 'login.html',{'msg':'Password Incorrect!!'})
            except:
                return render(request, 'login.html', {'msg':'Email is not Registered!!'})
        return render(request, 'login.html')
           
        
def logout(request):
    try:
        request.session['email']
        del request.session['email']
        return render(request, 'login.html')
    except:
        return render(request,'login.html',{'msg':'Cannot logout without login'})
    

def arrival(request):
    all_products = Products.objects.all()
    return render(request, 'arrival.html',{'all_products':all_products})

def profile_buyer(request):
    session_user = User.objects.get(email = request.session['email'])
    if request.method=='POST':
        if request.FILES:
            if request.POST['cpassword']:
                if request.POST['password']==request.POST['cpassword']:
                    session_user.fullname = request.POST['fname']
                    session_user.password = request.POST['password']
                    session_user.pic=request.FILES['pic']
                    session_user.save()
                    return render(request, 'profile_buyer.html',{'session_user':session_user,'msg':'UPDATED SUCCESSFULLY !!!!'})
                else:
                    return render(request, 'profile_buyer.html',{'session_user':session_user,'msg':'Passwords not match'})
            else:
                session_user.fullname = request.POST['fname']
                session_user.password = request.POST['password']
                session_user.pic=request.FILES['pic']
                session_user.save()
                return render(request, 'profile_buyer.html',{'session_user':session_user,'msg':'UPDATED SUCCESSFULLY !!!!'})
        else:
            if request.POST['cpassword']:
                if request.POST['password']==request.POST['cpassword']:
                    session_user.fullname = request.POST['fname']
                    session_user.password = request.POST['password']
                    session_user.save()
                    return render(request, 'profile_buyer.html',{'session_user':session_user,'msg':'UPDATED SUCCESSFULLY !!!!'})
                else:
                    return render(request, 'profile_buyer.html',{'session_user':session_user,'msg':'Passwords not match'})
            else:
                session_user.fullname = request.POST['fname']
                session_user.password = request.POST['password']
                session_user.save()
                return render(request, 'profile_buyer.html',{'session_user':session_user,'msg':'UPDATED SUCCESSFULLY !!!!'})
    return render(request, 'profile_buyer.html',{'session_user':session_user})

def fpassword_buyer(request):
    if request.method=='POST':
        try:
         session_user = User.objects.get(email = request.POST['email'])
         mail = session_user.password
         subject = 'Welcome to Ecommerce '
         message = f'Your Password is {mail}'
         email_from = settings.EMAIL_HOST_USER
         recipient_list = [request.POST['email'], ]
         send_mail( subject, message, email_from, recipient_list )
         return render(request,'login.html',{'msg':'Password Sent to Mail'})
        except:
            return render(request,'fpassword_buyer.html',{'msg':'Email Not Found!!! Please enter correct email'})
    return render(request,'fpassword_buyer.html')

def add_to_cart(request, pk):
    session_user=User.objects.get(email=request.session['email'])
    pid = Products.objects.get(id=pk)
    Cart.objects.create(
        userid=session_user,
        productid=pid,
        orderid=order_id,
    )
    all_products = Products.objects.all()
    return render(request, 'arrival.html',{'all_products':all_products})


def cart(request):
    try:
        session_user=User.objects.get(email=request.session['email'])
        cart_data = Cart.objects.filter(userid = session_user, orderid=order_id)
        print(cart_data)
        return render(request, 'cart.html',{'cart_data':cart_data})
    except NameError:
        return redirect('login')
    except KeyError:
        return redirect('login')

def remove_cart(request, pk):
    prod=Cart.objects.get(id=pk)
    prod.delete()
    session_user=User.objects.get(email=request.session['email'])
    cart_data = Cart.objects.filter(userid = session_user, orderid=order_id)
    print(cart_data)
    return render(request, 'cart.html',{'cart_data':cart_data})

def checkout(request):
    session_user=User.objects.get(email=request.session['email'])
    cart_data = Cart.objects.filter(userid = session_user)
    cart_data = cart_data.values()
    print(cart_data)
    single_amount = 0
    for x in cart_data:
        pro_price=Products.objects.get(id=x['productid_id'])
        single_amount+=pro_price.price
    return render(request,'payment.html',{'msg':single_amount})