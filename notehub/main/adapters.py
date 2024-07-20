from datetime import datetime
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter 
from .models import SocialUsersProfile
from django.contrib.auth.models import User

class CustomAccountAdapter(DefaultSocialAccountAdapter ):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.username = user.email

        try:
            existing_user = User.objects.get(email=user.email)
            print("user already exists")
        except:
            extra_data = sociallogin.account.extra_data
            picture_url = extra_data.get('picture')

            profile = SocialUsersProfile(
                email = user.email,
                profile_url = picture_url,
                created_at = datetime.now(),
                updated_at = datetime.now()
            )
            profile.save()
        
        return user
