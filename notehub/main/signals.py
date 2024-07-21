from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import SocialUsersProfile, UserProfile
from datetime import datetime
from .utils import send_email

@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs):
    if created and not instance.has_usable_password():
        # This code will run when a new User instance is created
        social_user_profile_doc = SocialUsersProfile.objects.get(email=instance.username)
        user_profile_doc = UserProfile(
            user = instance,
            profile_url = social_user_profile_doc.profile_url,
            created_at = datetime.now(),
            updated_at = datetime.now()
        )
        user_profile_doc.save()
        social_user_profile_doc.delete()
        recipient = [instance.email]
        subject = 'Welcome Onboard !'
        template = 'welcome_and_verification_template.html'
        metadata = {'user': instance}
        send_email(recipient, subject, template, metadata)
