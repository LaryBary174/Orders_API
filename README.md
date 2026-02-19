# Сервис для управления заказами

Сервис управления заказами, поддерживающий аутентификацию, работу с очередями сообщений, кеширование и фоновую обработку задач


## Быстрый старт

### Установка

1. Клонирование репозитория
2. Настройка окружения
```
cp .env.example .env
# Отредактируйте при необходимости .env файл
```
3. Запуск 
```
docker-compose up --build
```
4. Применение миграции
```
# По имени контейнера
docker exec fastapi_app alembic upgrade head

# Или по имени сервиса
docker-compose exec web alembic upgrade head
```
5. Swagger
    - http://localhost:8000/docs
    - http://localhost:8000/redoc



