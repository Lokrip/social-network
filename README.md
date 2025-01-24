# Социальная сеть

Это проект социальной сети, разработанный с использованием Django. Приложение предоставляет широкий функционал, включая управление пользователями, чаты, публикации, уведомления, профили и многое другое. Проект настроен для работы в контейнерах Docker.

## Основные функции

- Регистрация и авторизация пользователей.
- Создание, редактирование и удаление публикаций.
- Система чатов для общения между пользователями.
- Управление профилями пользователей.
- Уведомления о действиях других пользователей.
- Хранение и отображение медиафайлов (аватарки, изображения публикаций и т.д.).
- Администрирование через Django Admin.
- Локализация приложения.

## Структура проекта

Проект организован следующим образом:

- **account** - управление учетными записями пользователей.
- **appSerilizers** - сериализаторы для API.
- **chat** - система чатов.
- **database** - файлы для настройки и миграции базы данных.
- **home** - главная страница социальной сети.
- **media** - каталог для хранения медиафайлов.
- **services** - логика для сторонних сервисов.
- **settings** - конфигурация проекта.
- **slices** - управление бизнес-логикой.
- **socialTemplate** - шаблоны для отображения интерфейса.
- **static** - статические файлы (CSS, JS, изображения).
- **templates** - HTML-шаблоны.
- **utils** - вспомогательные утилиты.
- **Dockerfile** - файл для сборки Docker-образа.
- **docker-compose.yml** - конфигурация для запуска Docker-контейнеров.
- **requirements.txt** - зависимости проекта.
- **manage.py** - основной скрипт для управления Django-проектом.

## Установка

### Требования

1. Docker и Docker Compose.
2. Python 3.8 или выше (если работаете без Docker).

### Быстрый старт с Docker

1. Клонируйте репозиторий:

```bash
git clone https://github.com/ваш-проект/social-network.git
cd social-network
```

2. Запустите Docker Compose:

```bash
docker-compose up --build
```

3. После успешного запуска проекта приложение будет доступно по адресу http://127.0.0.1:8000


### Установка без Docker (опционально)

1. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Выполните миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

2. Создайте файл .env в корне проекта и добавьте необходимые переменные окружения, например: 

```bash
DEBUG=True
SECRET_KEY=ваш-секретный-ключ
DB_NAME=social_network_db
DB_USER=postgres
DB_PASSWORD=пароль
DB_HOST=db
DB_PORT=5432
```


4. Запустите сервер разработки:


```bash
python manage.py runserver
```
