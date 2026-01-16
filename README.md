# Автосервис74

## Сборка проекта
    docker compose --env-file .env -f docker-compose.yml build

## Запуск сервиса
    docker compose --env-file .env -f docker-compose.yml up
#### Сервисы будет доступен по адресам:
    Gateway         http://127.0.0.1:8000
    User-Service    http://127.0.0.1:8001    
    Product-Service http://127.0.0.1:8002    
    Order-Service   http://127.0.0.1:8003

#### Документация:
    User-Service    http://127.0.0.1:8001/docs    
    Product-Service http://127.0.0.1:8002/docs    
    Order-Service   http://127.0.0.1:8003/docs

## Остановка сервиса
	docker compose --env-file .env -f docker-compose.yml down

## Запуск тестов
    docker exec user-service pytest tests -s -v
    docker exec product-service pytest tests -s -v
    docker exec order-service pytest tests -s -v