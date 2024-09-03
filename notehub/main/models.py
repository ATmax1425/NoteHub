from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_url = models.URLField(default="https://cdn.pixabay.com/photo/2012/04/26/19/43/profile-42914_640.png")

    def __str__(self):
        return self.user.username

class SocialUsersProfile(BaseModel):
    email = models.EmailField()
    profile_url = models.URLField()

    def __str__(self):
        return self.email

class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Document(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    file_url = models.URLField(max_length=500)
    file_size = models.IntegerField(default=0)
    file_type = models.CharField(max_length=100, default="Text Document")
    tags = models.ManyToManyField(Tag, blank=True, related_name='documents')

    def __str__(self):
        return self.title