# API приложения для совместных пробежек

API разработано с применением фреймворка FastAPI. 

База данных: PostgreSQL, ORM: SQLAlchemy. 

Обработка задач: Celery + Redis

## Что реализовано:
___________________________________________

- Профили пользователей с возможностью добавления/изменения данных о себе. А также получение данных других пользователей (просмотр)


- Регистрация, аутентификация и авторизация пользователей через access и refresh JWT. Токены генерируются на основе приватного и публичного ключей;


- Подтверждение регистрации по email. Если почта не подтверждена, то доступ к изменению данных запрещен


## Запуск приложения
___________________________________________

### 1. Создать файл c переменными окружения и поместить его в корневую папку приложения

".env" - для запуска приложения без Docker

".env-non-dev" - для запуска приложения с Docker

Пример файла с необходимыми переменными окружения: docs/.env-example

### 2. Сгенерировать приватный и публичный секретные ключи для генерации JWT

Например, приватный ключ можно сгенерировать так:
````
openssl genrsa -out src/auth/certs/jwt-private.pem 2048
````
И затем на основе приватного ключа сгенерировать публичный ключ:
````
openssl rsa -in src/auth/certs/jwt-private.pem -outform PEM -pubout -out src/auth/certs/jwt-public.pem
````

### 3. Запустить приложение без Docker

Важно! Перед запуском приложения в вашей системе должны быть установлены PostgreSQL и Redis. 

Кроме этого, в приложении не предусмотрена работа с Celery на Windows. Если у вас Windows, и вы хотите работать с Celery, рассмотрите вариант запуска через Docker, описанный ниже.

- Установить зависимости:
````
pip install -r requirements-main.txt
````

- Установить зависимости для тестирования (опционально):
````
pip install -r requirements-test.txt
````

- Установить зависимости инструментов разработки (опционально):
````
pip install -r requirements-dev.txt
````

- Запустить приложение:
````
uvicorn src.main:app --reload
````

### 4. Запустить приложение с Docker

Будут запущены 7 Docker-контейнеров, в числе которых есть контейнер с тестами.

- Установить Docker и Docker Compose:
````
sh scripts/docker/docker.sh
````

- Запустить приложение в контейнерах:
````
sudo docker-compose up
````

## Инструменты разработки (опционально)
___________________________________________

Установить зависимости инструментов разработки:
````
pip install -r requirements-dev.txt
````

Для запуска линтера flake8:
````
flake8 --config .flake8 .
````

Для запуска форматтера isort:
````
isort --settings-file .isort.cfg .
````

Установить pre-commit хук для автоматического запуска flake8 и isort перед каждым коммитом в Git:
````
pre-commit install
````
