from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    profile_image = models.ImageField(upload_to='profiles/')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.user.username

class SocialUsersProfile(models.Model):
    email = models.EmailField()
    profile_url = models.URLField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.email
