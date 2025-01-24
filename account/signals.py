from django.dispatch import receiver
from django.db.models.signals import post_save

from database.models import GenerateCodeConfirmationEmail

from .tasks import delete_expired_token_one


@receiver(post_save, sender=GenerateCodeConfirmationEmail)
def code_postsave(sender, instance, created, **kwargs):
    confirmation = instance
    
    if created:
        delete_expired_token_one.apply_async((confirmation.pk,), countdown=600)