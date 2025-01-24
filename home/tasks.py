from django.shortcuts import get_object_or_404

from services.celery import app

from celery.exceptions import MaxRetriesExceededError

@app.task(bind=True, default_retry_delay=5 * 60, max_retries=10)
def deleting_story(self, story_id):
    from database.models import Story
    try:
        story = get_object_or_404(Story, pk=story_id)
        
        if story.is_expired():
            story.delete()
        else:
            raise self.retry()
        
    except Story.DoesNotExist:
        self.retry(countdown=60)
        
    except MaxRetriesExceededError:
        pass