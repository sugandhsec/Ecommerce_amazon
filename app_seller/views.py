from app_seller.models import Products, User_seller
from random import randrange
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail



# Create your views here.
def index_seller(request):
     try:
        request.session['email']
        session_user_data = User_seller.objects.get(email = request.session['email'])
        return render(request,'index_seller.html',{'user_data':session_user_data})
     except:
        return render(request,'index_seller.html')

def register_seller(request):
    if request.method == 'POST':
        try:
            User_seller.objects.get(email = request.POST['email'])
            return render(request, 'register_seller.html',{'msg':'Email is already registered'})
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

                return render(request, 'otp_seller.html')
            else:
                return render(request, 'register_seller.html',{'msg':'Both passwords is not same'})
    else:
        return render(request, 'register_seller.html')

def otp_seller(request):
    if request.method == 'POST':
        if int(request.POST['otp']) == otp:
            User_seller.objects.create(
                fullname = temp['fullname'],
                email = temp['email'],
                password = temp['password'],
            )
            return render(request, 'login_seller.html', {'msg': 'Successfully Registered!!'})
        else:
            return render(request, 'otp_seller.html', {'msg': 'seller otp wrong!!'})
    else:
        return render(request,'otp_seller.html')

def login_seller(request):
    try:
        request.session['email']
        session_user_data = User_seller.objects.get(email = request.session['email'])
        return render(request,'index_seller.html',{'user_data':session_user_data})
    except:
        if request.method == 'POST':
            try:
                uid = User_seller.objects.get(email = request.POST['email'])
                if request.POST['password'] ==  uid.password:
                    request.session['email'] = request.POST['email']
                    session_user_data = User_seller.objects.get(email = request.session['email'])
                    return render(request, 'index_seller.html',{'user_data':session_user_data})
                else:
                    return render(request, 'login_seller.html',{'msg':'Password Incorrect!!'})
            except:
                return render(request, 'login_seller.html', {'msg':'Email is not Registered!!'})
        return render(request, 'login_seller.html')
           


def logout_seller(request):
    try:
        request.session['email']
        del request.session['email']
        return render(request, 'login_seller.html')
    except:
        return render(request,'login_seller.html',{'msg':'Cannot logout without login'})
    
def add_product_seller(request):
    try:
        session_seller = User_seller.objects.get(email = request.session['email'])
        if request.method == 'POST':
            if request.FILES:
                Products.objects.create(
                    pname = request.POST['pname'],
                    price = request.POST['price'],
                    pic = request.FILES['pic'],
                    seller = session_seller
                )
                return render(request, 'add_product_seller.html', {'msg':'Created!!!','user_data':session_seller})
            else:
                Products.objects.create(
                    pname = request.POST['pname'],
                    price = request.POST['price'],
                    seller = session_seller
                )
                return render(request, 'add_product_seller.html', {'msg':'Created!!!','user_data':session_seller})
        return render(request, 'add_product_seller.html',{'user_data':session_seller})
    except:
        return render(request, 'login_seller.html')
    

def profile_seller(request):
    session_user =User_seller.objects.get(email=request.session['email'])
    if request.method=='POST':
        if request.FILES:
            if request.POST['cpassword']:
                if request.POST['password']==request.POST['cpassword']:
                    session_user.fullname = request.POST['fname']
                    session_user.password = request.POST['password']
                    session_user.pic=request.FILES['pic']
                    session_user.save()
                    return render(request, 'profile_seller.html',{'session_user':session_user,'msg':'UPDATED SUCCESSFULLY !!!!','user_data':session_user})
                else:
                    return render(request, 'profile_seller.html',{'session_user':session_user,'msg':'Passwords not match','user_data':session_user})
            else:
                session_user.fullname = request.POST['fname']
                session_user.password = request.POST['password']
                session_user.pic=request.FILES['pic']
                session_user.save()
                return render(request, 'profile_seller.html',{'session_user':session_user,'msg':'UPDATED SUCCESSFULLY !!!!','user_data':session_user})
        else:
            if request.POST['cpassword']:
                if request.POST['password']==request.POST['cpassword']:
                    session_user.fullname = request.POST['fname']
                    session_user.password = request.POST['password']
                    session_user.save()
                    return render(request, 'profile_seller.html',{'session_user':session_user,'msg':'UPDATED SUCCESSFULLY !!!!','user_data':session_user})
                else:
                    return render(request, 'profile_seller.html',{'session_user':session_user,'msg':'Passwords not match','user_data':session_user})
            else:
                session_user.fullname = request.POST['fname']
                session_user.password = request.POST['password']
                session_user.save()
                return render(request, 'profile_seller.html',{'session_user':session_user,'msg':'UPDATED SUCCESSFULLY !!!!','user_data':session_user})
    return render(request, 'profile_seller.html',{'session_user':session_user,'user_data':session_user})

def fpassword_seller(request):
    if request.method=='POST':
        try:
         session_user = User_seller.objects.get(email = request.POST['email'])
         mail = session_user.password
         subject = 'Welcome to Ecommerce '
         message = f'Your Password is {mail}'
         email_from = settings.EMAIL_HOST_USER
         recipient_list = [request.POST['email'], ]
         send_mail( subject, message, email_from, recipient_list )
         return render(request,'login_seller.html',{'msg':'Password Sent to Mail','user_data':session_user})
        except:
            return render(request,'fpassword_seller.html',{'msg':'Email Not Found!!! Please enter correct email'})
    return render(request,'fpassword_seller.html')