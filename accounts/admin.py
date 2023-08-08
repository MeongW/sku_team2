from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import SMSAuthentication

CustomUser = get_user_model()
#admin.site.register(CustomUser)

@admin.register(CustomUser)
class CustomUserModelAdmin(admin.ModelAdmin):
    pass

@admin.register(SMSAuthentication)
class SMSAuthenticationModelAdmin(admin.ModelAdmin):
    pass