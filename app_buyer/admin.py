from django.contrib import admin
from app_buyer.models import User,Cart

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display= ['fullname', 'email', 'password','pic']

admin.site.register(Cart)