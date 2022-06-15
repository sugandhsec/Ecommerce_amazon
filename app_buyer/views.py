#/home/sugandhanywhere/Ecommerce_amazon/app_seller
#/home/sugandhanywhere/Ecommerce_amazon/app_buyer

from random import randrange

from django.http import HttpResponseBadRequest
import razorpay
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from app_buyer.models import User,Cart
from app_seller.models import Products

from . import *

# Create your views here.
def index(request):
    try:
        session_user_data = User.objects.get(email = request.session['email'])
        return render(request,'index.html',{'user_data':session_user_data})
    except:
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
    session_user_data = User.objects.get(email = request.session['email'])
    all_products = Products.objects.all()
    return render(request, 'arrival.html',{'all_products':all_products,'user_data':session_user_data})

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
                    return render(request, 'profile_buyer.html',{'session_user':session_user,'msg':'UPDATED SUCCESSFULLY !!!!','user_data':session_user})
                else:
                    return render(request, 'profile_buyer.html',{'session_user':session_user,'msg':'Passwords not match','user_data':session_user})
            else:
                session_user.fullname = request.POST['fname']
                session_user.password = request.POST['password']
                session_user.pic=request.FILES['pic']
                session_user.save()
                return render(request, 'profile_buyer.html',{'session_user':session_user,'msg':'UPDATED SUCCESSFULLY !','user_data':session_user})
        else:
            if request.POST['cpassword']:
                if request.POST['password']==request.POST['cpassword']:
                    session_user.fullname = request.POST['fname']
                    session_user.password = request.POST['password']
                    session_user.save()
                    return render(request, 'profile_buyer.html',{'session_user':session_user,'msg':'UPDATED SUCCESSFULLY !!','user_data':session_user})
                else:
                    return render(request, 'profile_buyer.html',{'session_user':session_user,'msg':'Passwords not match','user_data':session_user})
            else:
                session_user.fullname = request.POST['fname']
                session_user.password = request.POST['password']
                session_user.save()
                return render(request, 'profile_buyer.html',{'session_user':session_user,'msg':'UPDATED SUCCESSFULLY !!!','user_data':session_user})
    return render(request, 'profile_buyer.html',{'session_user':session_user,'user_data':session_user})

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
    return render(request, 'arrival.html',{'all_products':all_products,'user_data':session_user})


def cart(request):
    try:
        session_user=User.objects.get(email=request.session['email'])
        cart_data = Cart.objects.filter(userid = session_user, orderid=order_id)        
        return render(request, 'cart.html',{'cart_data':cart_data,'user_data':session_user})
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
    return render(request, 'cart.html',{'cart_data':cart_data,'user_data':session_user})

# def checkout(request):
#     session_user=User.objects.get(email=request.session['email'])
#     cart_data = Cart.objects.filter(userid = session_user)
#     cart_data = cart_data.values()
#     global single_amount
#     single_amount = 0
#     for x in cart_data:
#         pro_price=Products.objects.get(id=x['productid_id'])
#         single_amount+=pro_price.price

#     # For Razorpay
#         currency = 'INR'
#         amount = single_amount  # Rs. 200
    
#         # Create a Razorpay Order
#         razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                         currency=currency,
#                                                         payment_capture='0'))
    
#         # order id of newly created order.
#         razorpay_order_id = razorpay_order['id']
#         callback_url = 'paymenthandler/'
    
#         # we need to pass these details to frontend.
#         context = {}
#         context['razorpay_order_id'] = razorpay_order_id
#         context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#         context['razorpay_amount'] = amount
#         context['currency'] = currency
#         context['callback_url'] = callback_url

#     return render(request,'payment.html',{'amount':single_amount},context)


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def checkout(request):
    currency = 'INR'
    session_user=User.objects.get(email=request.session['email'])
    cart_data = Cart.objects.filter(userid = session_user)
    cart_data = cart_data.values()
    global single_amount
    single_amount = 0
    for x in cart_data:
        pro_price=Products.objects.get(id=x['productid_id'])
        single_amount+=pro_price.price #Rupiya
    amount_user_show = single_amount # Rupiya
    amount = single_amount*100 # Paise


    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['amount']= amount_user_show
    return render(request, 'payment.html', context=context)
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            # result = razorpay_client.utility.verify_payment_signature(
            #     params_dict)
            # if result is None:
            amount = single_amount*100  # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)

                # render success page on successful caputre of payment
                session_user=User.objects.get(email=request.session['email'])
                cart_data = Cart.objects.filter(userid = session_user)
                cart_data.delete()
                return render(request, 'paymentsuccess.html')
            except:

                # if there is an error while capturing payment.
                return render(request, 'paymentfail.html')
            # else:
 
            #     # if signature verification fails.
            #     return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
# Note: It is necessary to capture the payment, otherwise it would be auto refunded to