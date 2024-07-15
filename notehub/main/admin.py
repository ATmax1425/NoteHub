from django.contrib import admin
from .models import UserProfile, SocialUsersProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_image', 'created_at', 'updated_at']

@admin.register(SocialUsersProfile)
class SocialUsersProfileAdmin(admin.ModelAdmin):
    list_display = ['email', 'profile_url', 'created_at', 'updated_at', 'deleted']
