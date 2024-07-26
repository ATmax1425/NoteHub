from django.contrib import admin
from .models import UserProfile, SocialUsersProfile, Tag, Document

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_url', 'created_at', 'updated_at']

@admin.register(SocialUsersProfile)
class SocialUsersProfileAdmin(admin.ModelAdmin):
    list_display = ['email', 'profile_url', 'created_at', 'updated_at']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'author', 'file_url', 'created_at', 'updated_at']