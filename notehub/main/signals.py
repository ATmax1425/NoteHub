from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.cache import cache
from django.conf import settings
from .models import SocialUsersProfile, UserProfile, Document
from datetime import datetime
from .utils import send_verification_email, send_email
from .documents import DocumentDocument

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

@receiver(post_delete, sender=User)
def user_deleted_handler(sender, instance, **kwargs):
    recipients = [instance.username]
    subject = 'Sorry to see you go!'
    template = 'goodbye_user.html'
    metadata = {'user': instance}
    send_email(recipients, subject, template, metadata)


@receiver(post_save, sender=Document)
def index_document(sender, instance, **kwargs):
    DocumentDocument().update(instance)
    
@receiver(post_delete, sender=Document)
def delete_document(sender, instance, **kwargs):
    DocumentDocument().delete(instance)
