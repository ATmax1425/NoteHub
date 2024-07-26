from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_url = models.URLField(default="https://cdn.pixabay.com/photo/2012/04/26/19/43/profile-42914_640.png")
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.user.username

class SocialUsersProfile(models.Model):
    email = models.EmailField()
    profile_url = models.URLField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.email
