from app_seller import views
from django.urls import  path

urlpatterns = [
    path('',views.index_seller,name="index_seller"),
    path('register_seller/',views.register_seller, name="register_seller"),
    path('otp_seller/',views.otp_seller, name="otp_seller"),
    path('login_seller/',views.login_seller, name="login_seller"),
    path('logout_seller/',views.logout_seller, name="logout_seller"),
    path('add_product_seller/',views.add_product_seller, name="add_product_seller"),
    path('profile_seller/',views.profile_seller, name="profile_seller"),
    path('fpassword_seller/',views.fpassword_seller, name="fpassword_seller"),
]
