# Автосервис74

## Сборка проекта
    docker compose --env-file .env -f docker-compose.yml build

## Запуск сервиса
    docker compose --env-file .env -f docker-compose.yml up
Сервис будет доступен по адресу: http://127.0.0.1:8001

Документация: http://127.0.0.1:8001/docs

## Остановка сервиса
	docker compose --env-file .env -f docker-compose.yml down

## Запуск тестов
    docker exec user-service pytest tests -s -v