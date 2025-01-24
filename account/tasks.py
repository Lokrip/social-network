from datetime import datetime

from services.celery import app
from database.models import GenerateCodeConfirmationEmail

from .service import send

@app.task
def send_email(user_id, uuid_code):
    from database.models import User
    user = User.objects.get(pk=user_id)
    return send(user=user, uuid_code=uuid_code)


@app.task
def delete_expired_tokens():
    now = datetime.now()
    
    expired_tokens = GenerateCodeConfirmationEmail.objects.filter(expiry_time__lt=now)
    if expired_tokens.exists():
        expired_count = expired_tokens.count()
        expired_tokens.delete()
        return f"{expired_count} токены с истекшим сроком действия удалены."
    return "Токены не найден или не истекли."

@app.task
def delete_expired_token_one(GCCE_id):
    now = datetime.now()
    expired_token = GenerateCodeConfirmationEmail.objects.filter(pk=GCCE_id, expiry_time__lt=now).first()
    if expired_token:
        expired_token_id = expired_token.pk
        expired_token.delete()
        return f"{expired_token_id} токены с истекшим сроком действия удален."
    return "Токен не найден или не истек."