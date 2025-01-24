from django.urls import reverse
from django.http import HttpRequest

from database.models import (
    Story,
    Notification
)


class ConfigContext:
    def __init__(self, is_start):
        self.is_start = is_start
        
    def initialize(self):
        """
        Выполняет инициализацию, если is_start равно True.
        
        :raises ValueError: Если is_start равно False.
        """
        if not self.is_start:
            raise ValueError("Инициализация невозможна: is_start должен быть True.")
        # Выполнить инициализационные действия здесь
        print("Инициализация завершена успешно.")

class ContextProcessors(ConfigContext):
    def __init__(self, request: HttpRequest, is_start):
        super().__init__(is_start)
        self.request = request
        
    def process(self):
        """
        Метод для обработки контекста.
        """
        raise NotImplementedError("Метод 'process' должен быть реализован в подклассе.")

class StoryProcessors(ContextProcessors):
    def __init__(self, request: HttpRequest, is_start):
        super().__init__(request, is_start)
        
    def process(self):
        return {"story": self.get_story()}
        
    def get_story(self):
        """
        Возвращает историю пользователя или None, если история не найдена.
        """
        try:
            story = Story.objects.get(user=self.request.user)
            return story
        except Story.DoesNotExist:
            return None
    
class HeaderProcessors(ContextProcessors):
    def __init__(self, request: HttpRequest, is_start):
        super().__init__(request, is_start)
        
    def process(self):
        return {'navbar_header': self.get_navbar_header()}
        
    @staticmethod
    def get_navbar_header():
        """
        Возвращает список меню для навбара.
        """
        MENU = [
            {
                "name": "home",
                "icon": "feather-home font-lg alert-primary btn-round-lg theme-dark-bg text-current",
                "href": reverse('social-home:home'),
            },
            {
                "name": "stories",
                "icon": "feather-zap font-lg bg-greylight btn-round-lg theme-dark-bg text-grey-500",
                "href": '',
            },
            {
                "name": "videos",
                "icon": "feather-video font-lg bg-greylight btn-round-lg theme-dark-bg text-grey-500",
                "href": reverse('slices-home:home'),
            },
            {
                "name": "groups",
                "icon": "feather-user font-lg bg-greylight btn-round-lg theme-dark-bg text-grey-500",
                "href": '',
            },
            {
                "name": "shop",
                "icon": "feather-shopping-bag font-lg bg-greylight btn-round-lg theme-dark-bg text-grey-500",
                "href": '',
            },
        ]
        return MENU

class NotificationProcessors(ContextProcessors):
    def __init__(self, request: HttpRequest, is_start):
        super().__init__(request, is_start)
    
    def process(self):
        return {'notifications': self.get_notifications()}  
    
    def get_notifications(self):
        if self.request.user.is_authenticated:
            return Notification.objects.prefetch_related("sender").filter(
                recipient=self.request.user
            )
        return []