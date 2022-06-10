from django.urls import path
from app_buyer import views

urlpatterns = [
    path('',views.index,name="index"),
    path('register/',views.register, name="register"),
    path('otp/',views.otp, name="otp"),
    path('login/',views.login, name="login"),
    path('logout/',views.logout, name="logout"),
    path('arrival/',views.arrival, name="arrival"),
    path('profile_buyer/',views.profile_buyer, name="profile_buyer"),
    path('fpassword_buyer/',views.fpassword_buyer, name="fpassword_buyer"),
    path('add_to_cart/<int:pk>',views.add_to_cart, name="add_to_cart"),
    path('remove_cart/<int:pk>',views.remove_cart, name="remove_cart"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path('checkout/paymenthandler/', views.paymenthandler, name='paymenthandler'),
]
