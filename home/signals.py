from django.dispatch import receiver
from django.db.models.signals import post_save
from database.models import Story
from .tasks import deleting_story

@receiver(post_save, sender=Story)
def story_delete_postsave(sender, instance, created, **kwargs):
    if created:
        print('created')
        deleting_story.apply_async((instance.pk,), countdown=60)