import random

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from django.db import transaction

from database.models import (
    User,
    GenerateCodeConfirmationEmail
)

from services.settings import EMAIL_HOST_USER


def generate_unique_code(length: int):
    while True:
        # Generate a string of random digits, not a list
        code = ''.join([str(random.randint(0, 9)) for _ in range(length)])
        if not GenerateCodeConfirmationEmail.objects.filter(code=code).exists():
            return code

        

def send(user: User, uuid_code):
    subject = 'Confirm Your Email'
    from_email = EMAIL_HOST_USER
    random_numbers = generate_unique_code(6)
    
    to = user.email
    
    #transaction.atomic — это основной инструмент для управления транзакциями. Он позволяет гарантировать, что все операции в рамках блока будут выполнены или откатятся, если произойдёт ошибка
    with transaction.atomic(): 
        confirmation = GenerateCodeConfirmationEmail.objects.create(
            user=user,
            code=random_numbers,
            uuid=uuid_code,
        )

    
    #html код переобразуем в строку тоесть теги будут строкой тоесть "<h1>Hello world</h1>" as string и мы можем вывести print потому что он теперь строка
    html_content = render_to_string('account/email/confirm-email-code.html', {
        'title': 'Code is active',
        'random_numbers': random_numbers
    })
    
    #удаляет теги с строки
    text_content = strip_tags(html_content)
    
    # Создаем объект EmailMultiAlternatives для отправки письма с текстовой и HTML версией
    email = EmailMultiAlternatives(subject, text_content, from_email, [to])
    
    # Добавляем HTML-версию как альтернативу
    email.attach_alternative(html_content, 'text/html')
    
    #send отпровляет письмо
    email.send()
    
    return confirmation.uuid