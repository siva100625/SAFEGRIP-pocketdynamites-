from django.contrib import admin
from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
# # Customize the UserAdmin to display only the username
# class UserAdmin(BaseUserAdmin):
#     model = User
#     list_display = ('username',)  # Display only the username field
#     search_fields = ('username',)  # Search by username

# admin.site.unregister(User)  # Unregister the default User admin
# admin.site.register(User)

admin.site.register(models.SensorData)
