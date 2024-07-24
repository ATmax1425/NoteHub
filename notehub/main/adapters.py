from datetime import datetime
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter 
from .models import SocialUsersProfile
from allauth.core.exceptions import ImmediateHttpResponse
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import redirect
from django.contrib.auth import login as login_user

AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'

class CustomAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        if email:
            user = None
            try:
                user = User.objects.get(email=email)
            except Exception as exc:
                print('New user signup')
            if user and not SocialAccount.objects.filter(user=user, provider=sociallogin.account.provider).exists():
                sociallogin.connect(request, user)
                login_user(request, user, AUTH_BACKEND)
                raise ImmediateHttpResponse(redirect('index'))

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.username = user.email

        try:
            existing_user = User.objects.get(email=user.email)
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
