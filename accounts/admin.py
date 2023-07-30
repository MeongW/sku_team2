from django.contrib import admin
from django.contrib.auth import get_user_model

CustomUser = get_user_model()
#admin.site.register(CustomUser)

@admin.register(CustomUser)
class CustomUserModelAdmin(admin.ModelAdmin):
    pass