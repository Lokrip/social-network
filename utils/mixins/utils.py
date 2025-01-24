from datetime import timedelta

from django.utils import timezone
from abc import ABC, abstractmethod

class IUtils(ABC):
    @abstractmethod
    def default_expiry_time():
        pass

class Utils(IUtils):
    @classmethod
    def default_expiry_time(cls):
        return timezone.now() + timedelta(minutes=10)

class ILoggerUtils(ABC):
    @abstractmethod
    def logger(self, topic: str = None) -> list:
        raise NotImplementedError

class LoggerUtils(ILoggerUtils):
    def logger(topic: str = None) -> list:
        """
        Логгер, возвращающий сообщения об ошибках для заданной темы.

        Parameters:
            topic (str): Категория, для которой нужны сообщения лога.

        Returns:
            list: Список сообщений, связанных с заданной темой.

        Raises:
            ValueError: Если limitLogger <= 0 или тема не найдена.
        """

        loggers = {
            'search': [
                'No results found for the search query',  # Когда поиск не дал результатов
                'Search query is too short',             # Когда запрос слишком короткий
                'Search service is currently unavailable'  # Когда поиск временно недоступен
            ],

            'authentication': [
                'Invalid username or password',          # Когда данные для входа неверны
                'Account is locked due to multiple failed login attempts',  # Блокировка из-за неудачных попыток
                'User account is inactive',              # Пользователь заблокирован
                'Session has expired'                    # Истек срок действия сессии
            ],

            'database': [
                'Database connection lost',              # Потеря соединения с БД
                'Failed to fetch data',                  # Не удалось получить данные
                'Data write failed'                      # Ошибка записи данных
            ],

            'file_upload': [
                'File type not supported',               # Тип файла не поддерживается
                'File size exceeds the limit',           # Превышен размер файла
                'File upload interrupted'                # Прерывание загрузки файла
            ],

            'payment': [
                'Payment gateway not responding',        # Проблема с платёжной системой
                'Payment declined by the bank',          # Отклонение платежа банком
                'Insufficient funds'                     # Недостаточно средств
            ]
        }

        if topic not in loggers:
            raise ValueError("Invalid topic provided")

        return loggers[topic]

class IFormUtility(ABC):
    @abstractmethod
    def validate_field(self, field_value):
        raise NotImplementedError
    
class FormUtility(IFormUtility):
    def validate_field(self, field_value):
        return field_value is not None and len(field_value) > 0


