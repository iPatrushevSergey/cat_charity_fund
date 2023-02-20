![Python](https://img.shields.io/pypi/pyversions/scrapy?color=brightgreen&style=plastic) ![FastAPI](https://img.shields.io/badge/FastAPI-0.78.0-brightgreen>) ![Starlette](https://img.shields.io/badge/Starlette-0.19.1-brightgreen>) ![Pydantic](https://img.shields.io/badge/Pydantic-1.9.1-brightgreen>) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4.36-brightgreen>) ![FastAPI-Users](https://img.shields.io/badge/FastAPIUsers-10.0.4-brightgreen>) ![Alembic](https://img.shields.io/badge/Alembic-1.7.7-brightgreen>)

# Проект 22-го спринта "Асинхронное API приложение QRKot"

## Описание

Благотворительный фонд поддержки котиков `QRKot` - собирает пожертвования на различные
целевые проекты: медицинское обслуживание, обустройство жилища, корм и любые другие цели,
связанные с поддержкой кошачьей популяции. Котану Ваську на прошлой неделе купили
зимний пуховик и построили собственный дом.

## Технологии

- Python 3.9
- FastAPI 0.78.0
- Starlette 0.19.1
- Pydantic 1.9.1
- SQLAlchemy 1.4.36
- FastAPI-Users 10.0.4
- Alembic 1.7.7

## Подготовка проекта

1. Необходимо сделать **Fork** репозитория:
```
https://github.com/iPatrushevSergey/cat_charity_fund.git
```
2. Далее нужно клонировать проект:
```
git clone git@github.com:<ваш_username>/cat_charity_fund.git
```
3. Создать и активировать виртуальное окружение:

- MacOS и Linux
```
python3 -m venv venv && . venv/bin/activate
```
- Windows
```
python -m venv venv && . venv/bin/activate
```
4. Установить зависимости:
```
pip install -r requirements.txt 
```
5. Внести в **.env** файл настройки базы данных - **DATABASE_URL**; секретное слово - **SECRET**; email и password суперюзера - **FIRST_SUPERUSER_EMAIL** и **FIRST_SUPERUSER_PASSWORD**; настройки почтового клиента - **MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM, MAIL_PORT, MAIL_SERVER, MAIL_FROM_NAME**.  

## Запуск проекта

```
app.main:app --reload
```

## Благотворительыне проекты в QRKot

В фонде QRKot может быть открыто несколько проектов, у каждого из которых есть название, описание и сумма, которую планируется собрать, количество инвестированных средств, дата создания и закрытия. Все пожертвования идут в проект, открытый раньше других. 

### Примеры API запросов

#### 1. Получение списка всех проектов:
GET-запрос /charity_project/

*Доступно всем пользователям*

> Ответ:
>```json
>[    
>    {
>       "name": "string",
>       "description": "string",
>       "full_amount": 0,
>       "id": 0,
>       "invested_amount": 0,
>       "fully_invested": true,
>       "create_date": "2019-08-24T14:15:22Z",
>       "close_date": "2019-08-24T14:15:22Z"
>    }
>]
>```

#### 2. Создание благотворительного проекта:
POST-запрос /charity_project/

*Обязательные поля*: **name**, **description**, **full_amount**

*Только для суперюзеров*

> Тело запроса:
>```json
>{
>    "name": "string",
>    "description": "string",
>    "full_amount": 0
>}
>```

> Ответ:
>```json
>{
>   "name": "string",
>   "description": "string",
>   "full_amount": 0,
>   "id": 0,
>   "invested_amount": 0,
>   "fully_invested": true,
>   "create_date": "2019-08-24T14:15:22Z",
>   "close_date": "2019-08-24T14:15:22Z"
>}
>```

#### 3. Удаление благотворительного проекта:
DELETE-запрос /charity_project/{project_id}

*Обязательный path-параметр*: **project_id**

*Только для суперюзеров*

> Ответ:
>```json
>{
>   "name": "string",
>   "description": "string",
>   "full_amount": 0,
>   "id": 0,
>   "invested_amount": 0,
>   "fully_invested": true,
>   "create_date": "2019-08-24T14:15:22Z",
>   "close_date": "2019-08-24T14:15:22Z"
>}
>```

#### 4. Обновление благотворительного проекта:
PATCH-запрос /charity_project/{project_id}

*Обязательный path-параметр*: **project_id**

*Только для суперюзеров*

> Тело запроса:
>```json
>{
>    "name": "string",
>    "description": "string",
>    "full_amount": 0
>}
>```

> Ответ:
>```json
>{
>    "name": "string",
>    "description": "string",
>    "full_amount": 0,
>    "id": 0,
>    "invested_amount": 0,
>    "fully_invested": true,
>    "create_date": "2019-08-24T14:15:22Z",
>    "close_date": "2019-08-24T14:15:22Z"
>}
>```

## Пожертвования в QRKot

Каждый вправе сделать пожертвование и написать к нему комментарий. Пожертвования не целевые, автоматически добавляются в первый открытый проект. При отсутствии проектов внесённые деньги ждут открытия следующего проекта, после чего автоматически вносятся в новый проект. 

### Примеры API запросов

#### 1. Получение всех пожертвований:
GET-запрос /donation/

*Только для суперюзеров*

> Ответ:
>```json
>[    
>    {
>        "full_amount": 0,
>        "comment": "string",
>        "id": 0,
>        "create_date": "2019-08-24T14:15:22Z",
>        "user_id": 0,
>        "invested_amount": 0,
>        "fully_invested": true,
>        "close_date": "2019-08-24T14:15:22Z"
>    }
>]
>```

#### 2. Создание пожертвования:
POST-запрос /donation/

*Обязательные поля*: **full_amount**

*Только для авторизованных пользователей*

> Тело запроса:
>```json
>{
>    "full_amount": 0,
>    "comment": "string"
>}
>```

> Ответ:
>```json
>{
>   
>    "full_amount": 0,
>    "comment": "string",
>    "id": 0,
>    "create_date": "2019-08-24T14:15:22Z"
>}
>```

#### 3. Получение всех пожертвований конкретного пользователя:
GET-запрос /donation/my

*Только для авторизованных пользователей*

> Ответ:
>```json
>[    
>    {
>        "full_amount": 0,
>        "comment": "string",
>        "id": 0,
>        "create_date": "2019-08-24T14:15:22Z"
>    }
>]
>```

## Регистрация и аутентификация

Регистрация и аутентификация пользователей. В проекте реализована возможность отправки писем успешно зарегистрированным пользователям.

### Примеры API запросов

#### 1. Регистрация пользователя:
POST-запрос /auth/register

> Тело запроса:
>```json
>{  
>    "email": "user@example.com",
>    "password": "string",
>    "is_active": true,
>    "is_superuser": false,
>    "is_verified": false
>}
>```

> Ответ:
>```json
>{
>    "id": null,
>    "email": "user@example.com",
>    "is_active": true,
>    "is_superuser": false,
>    "is_verified": false
>}
>```

#### 2. Аутентификация:
POST-запрос /auth/jwt/login

*Обязательные поля*: **username**, **password**

> Тело запроса:
>```json
>{  
>    "username": "user",
>    "password": "password",
>}
>```

> Ответ:
>```json
>{
>    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9yJ1c2VyX2lkIjoiOTIyMWZmYzktNjQ",
>    "token_type": "bearer"
>}
>```

#### 3. Разлогинивание:
POST-запрос /auth/jwt/logout

## Пользователи

В проекте реализована возможность автоматического создания суперпользователя.

### Примеры API запросов

#### 1. Текущий пользователь:
GET-запрос /users/me

*Только для авторизованных*

> Ответ:
>```json
>{
>    "id": 1,
>    "email": "user@example.com",
>    "is_active": true,
>    "is_superuser": false,
>    "is_verified": false
>}
>```

#### 2. Изменить свои данные:
PATCH-запрос /users/me

*Только для авторизованных пользователей*

> Тело запроса:
>```json
>{
>    "password": "string",
>    "email": "user@example.com",
>    "is_active": true,
>    "is_superuser": true,
>    "is_verified": true
>}
>```

> Ответ:
>```json
>{
>    "id": 1,
>    "email": "user@example.com",
>    "is_active": true,
>    "is_superuser": false,
>    "is_verified": false
>}
>```

#### 3. Получить пользователя по ID:
GET-запрос /donation/my

*Обязательный path-параметр*: **id**
*Только для авторизованных пользователей*

> Ответ:
>```json
>{
>    "id": 1,
>    "email": "user@example.com",
>    "is_active": true,
>    "is_superuser": false,
>    "is_verified": false
>}
>```

#### 4. Удаление пользователя:
GET-запрос /users/{id}

Функция удаления пользователей не предусмотрена. Необходимо деактивировать пользователей.

#### 5. Изменить данные конкретного пользователя:
PATCH-запрос /users/{id}

*Только для авторизованных пользователей*

> Тело запроса:
>```json
>{
>    "password": "string",
>    "email": "user@example.com",
>    "is_active": true,
>    "is_superuser": true,
>    "is_verified": true
>}
>```

> Ответ:
>```json
>{
>    "id": 1,
>    "email": "user@example.com",
>    "is_active": true,
>    "is_superuser": false,
>    "is_verified": false
>}
>```

+ **Author**: Patrushev Sergey
+ **Mail**: PatrushevSergeyVal@yandex.ru
+ **GitHub**: [iPatrushevSergey](https://github.com/iPatrushevSergey)
