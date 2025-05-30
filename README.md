## 📌 Beresnev Job Task
- Начало: 28.05.2025
- Завершение: 30.05.2025


### ⚙️ Технологии
- FastAPI
- Pytest
- SQLAlchemy
- Alembic
- PostgreSQL
- Docker
- Nginx
- Vue3


### Настройка в Docker

### Подготовка переменных окружения
Скопируйте файл .env.example в .env и заполните его следующим образом:
```ini
POSTGRES_DB_HOST=postgre_container
POSTGRES_DB_PORT=5432
POSTGRES_DB_USER=myuser
POSTGRES_DB_PASS=mypassword
POSTGRES_DB_NAME=main_postgresql_database

TEST_POSTGRES_DB_HOST=postgre_container_test
TEST_POSTGRES_DB_PORT=5432
TEST_POSTGRES_DB_USER=myuser
TEST_POSTGRES_DB_PASS=mypassword
TEST_POSTGRES_DB_NAME=test_postgresql_database
```

### Создание docker-сети
```bash
docker network create tasks-network
```

### Запуск сервисов основной БД и тестовой
```bash
docker compose -f docker-compose-services.yml up -d
```

### Сборка образа FastAPI-приложения
```bash
docker build -t fastapi-image-tasks-api -f backend/Dockerfile backend/
```

### Применение миграций Alembic
```bash
docker run --rm --network tasks-network --env-file .env fastapi-image-tasks-api alembic upgrade head
```

### Сборка образа VueJS-приложения + Nginx
```bash
docker build -t vuejs-image-tasks -f frontend/Dockerfile frontend/
```

### Запуск оброзов FastAPI + Vue3(nginx)
```bash
docker compose -f docker-compose.yml up -d
```

### Приложение
http://localhost/


### Запуск тестов с покрытием внутри контейнера
```bash
docker run --rm --network tasks-network --env-file .env fastapi-image-tasks-api pytest
```
