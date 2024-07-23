from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.cache import cache
from django.conf import settings
from .models import SocialUsersProfile, UserProfile
from datetime import datetime
from .utils import send_verification_email

@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs):
    # This code will run when a new User instance is created
    if created:
        send_verification_email(instance)
        if not instance.has_usable_password():
            social_user_profile_doc = SocialUsersProfile.objects.get(email=instance.username)
            user_profile_doc = UserProfile(
                user = instance,
                profile_url = social_user_profile_doc.profile_url,
                created_at = datetime.now(),
                updated_at = datetime.now()
            )
            user_profile_doc.save()
            social_user_profile_doc.delete()
