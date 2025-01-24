from settings.context.processors import (
    HeaderProcessors,
    NotificationProcessors
)

def get_context_django(request):
    """
    Контекстный процессор для добавления данных в шаблон.
    """
    is_start = True  
    header_processors = HeaderProcessors(request, is_start)
    notification_processors = NotificationProcessors(request, is_start)
    
    header_processors.initialize()
    notification_processors.initialize()
    
    print(notification_processors.process())

    return {
        **header_processors.process(),
        **notification_processors.process()
    }