"""
ASGI config for services project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.routing import (
    ProtocolTypeRouter,
    URLRouter 
)
from channels.auth import AuthMiddlewareStack

from django.core.asgi import get_asgi_application

from account.routing import account_urlpatterns
from chat.routing import chat_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            *account_urlpatterns,
            *chat_urlpatterns
        ])
    )
})
