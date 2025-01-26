from django.contrib import admin
from . import settings
from django.conf.urls.static import static
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='social-home')),
    path('slices/', include('slices.urls', namespace='slices-home')),
    path('chat/', include('chat.urls', namespace='chat-home')),
    path('account/', include('account.urls', namespace='account')),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
