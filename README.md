# purchases-accounting-REST API

## Опис
Набір API які надають можливість реєстрації, автентифікації та авторизації користувача, для створення та
перегляду чеків. Не зареєстровані користувачі мають можливість перегляду будь-якого створеного чека. 
Всі дані зберігаються в Postgres DB


### Запуск за допомогою Docker:
    
1. Клонуйте репозиторій на свою локальну машину:  

```bash
   git clone https://github.com/Igor-Cegelnyk/purchases-accounting-FastApi.git
   cd purchases-accounting-FastApi
```

2. Створіть образ Docker:

```bash
   docker-compose build
```

3. Запустіть контейнер:

```bash
   docker-compose up
```

### Документація API

Документація API доступна за адресою: http://localhost:8000/docs


### Локальний запуск сервера (Альтернативний варінт)

1. Клонуйте репозиторій на свою локальну машину, як зазначено вище
2. Створіть віртуальне оточення в корені проекту:

```
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
```

3. Якщо відсутній poetry:

```
pip install poetry
```

4. Встановіть залежності:

```
poetry install
```

5. Створіть директорію та згенеруйте приватний та публічний ключ:

```
mkdir backend\authentication\keys
cd backend\authentication\keys (on Windows)

mkdir -p backend/authentication/keys && cd $_ (on macOS)

openssl genrsa -out jwt-private.pem" 2048
openssl rsa -in "$KEYS_DIR/jwt-private.pem" -outform PEM -pubout -out jwt-public.pem"
```

6. Запустіть контейнер з Postgres

```
docker-compose up -d pg
```

7. Внеість зміни в файл backend/.env.template

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/purchases_accounting
```

8. Застосуйте міграцію в БД за допомогою alembic:

```
alembic upgrade head
```

9. Запустіть сервер:

```
uvicorn backend.main:app --reload
```