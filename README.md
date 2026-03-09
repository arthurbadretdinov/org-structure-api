# Organizational Structure API

API для управления организационной структурой компании: подразделениями и сотрудниками.

Проект реализует древовидную структуру подразделений и позволяет управлять сотрудниками внутри этих подразделений.

## Технологический стек

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic (миграции)
* Docker / docker-compose
* Pydantic

---

## Возможности API

API поддерживает следующие операции:

### Подразделения

* создание подразделения
* получение подразделения с поддеревом
* перемещение подразделения
* удаление подразделения

### Сотрудники

* создание сотрудника в подразделении
* получение сотрудников подразделения

---

## Модели

### Department

Подразделение компании.

| Поле       | Тип         | Описание                   |
| ---------- | ----------- | -------------------------- |
| id         | int         | идентификатор              |
| name       | str         | название подразделения     |
| parent_id  | int \| null | родительское подразделение |
| created_at | datetime    | дата создания              |

Связи:

* Department → Department (иерархия подразделений)
* Department → Employee (один ко многим)

---

### Employee

Сотрудник компании.

| Поле          | Тип          | Описание                     |
| ------------- | ------------ | ---------------------------- |
| id            | int          | идентификатор                |
| department_id | int          | идентификатор подразделения  |
| full_name     | str          | ФИО сотрудника               |
| position      | str          | должность                    |
| hired_at      | date \| null | дата найма                   |
| created_at    | datetime     | дата создания                |

---

## API endpoints

### Создать подразделение

POST `/departments/`

Body:

```json
{
  "name": "Backend",
  "parent_id": 1
}
```

Response:

```json
{
  "id": 3,
  "name": "Backend",
  "parent_id": 1,
  "created_at": "2026-03-08T12:00:00"
}
```

---

### Создать сотрудника

POST `/departments/{id}/employees/`

Body:

```json
{
  "full_name": "Ivan Ivanov",
  "position": "Backend Developer",
  "hired_at": "2024-01-01"
}
```

Response:

```json
{
  "id": 5,
  "department_id" : 3,
  "full_name": "Ivan Ivanov",
  "position": "Backend Developer",
  "hired_at": "2024-01-01",
  "created_at": "2026-03-08T12:00:00"
}
```

---

### Получить подразделение

GET `/departments/{id}`

Query параметры:

| параметр          | тип  | описание                                    |
| ----------------- | ---- | ------------------------------------------- |
| depth             | int  | глубина дерева (по умолчанию 1, максимум 5) |
| include_employees | bool | включать сотрудников                        |

Response:

```json
{
  "department": {},
  "employees": [],
  "children": []
}
```

---

### Обновить подразделение

PATCH `/departments/{id}`

Body:

```json
{
  "name": "Platform",
  "parent_id": 2
}
```

Response:

```json
{
  "id": 3,
  "name": "Platform",
  "parent_id": 2,
  "created_at": "2026-03-08T12:00:00"
}
```

---

### Удалить подразделение

DELETE `/departments/{id}`

Query параметры:

| параметр                  | описание                                     |
| --------------------------| -------------------------------------------- |
| mode=cascade              | удалить подразделение и всё поддерево        |
| mode=reassign             | сотрудников перевести в другое подразделение |
| reassign_to_department_id | номер подразделения, в которое перевести     |

---

Response: 204 No Content

## Бизнес-логика и ограничения

* Нельзя создать сотрудника в несуществующем подразделении.
* Название подразделения должно быть:

  * не пустым
  * длиной 1–200 символов
  * уникальным внутри одного родительского подразделения.
* Нельзя сделать подразделение родителем самого себя.
* Нельзя создавать циклы в дереве подразделений.
* Максимальная глубина вложенности в запросе — **5**.

---

## Запуск проекта

### Требования

* Docker
* Docker Compose

---

### Конфигурация через .env

Перед запуском проекта через Docker убедитесь, что в корне проекта есть файл `.env` со следующими переменными:

- `DB_USER` — пользователь PostgreSQL
- `DB_PASS` — пароль
- `DB_NAME` — имя базы данных
- `DB_HOST` — имя сервиса базы данных в docker-compose (`db`)
- `DB_PORT` — порт PostgreSQL

Этот файл нужен, чтобы FastAPI и Alembic могли подключиться к базе данных, и Docker корректно поднял сервисы.

### Запуск

Склонировать репозиторий:

```bash
git clone <repo_url>
cd organizational-structure-api
```

Запустить приложение:

```bash
docker compose --env-file .env down -v
docker compose --env-file .env up --build -d
```

После запуска API будет доступно:

```
http://localhost:8000
```

Swagger UI доступен по адресу:

```
http://localhost:8000/docs
```


ReDoc доступен по адресу:

```
http://localhost:8000/redoc
```


## Миграции базы данных

Миграции выполняются через Alembic.

Пример:

```bash
alembic upgrade head
```

---

## Структура проекта

```
app/
├─ main.py
├─ config.py    
├─ database.py
├─ enum.py
├─ exceptions.py
├─ utils.py
├─ db_validators.py
├─ models.py
├─ schemas.py
├─ router.py
├─ services.py
└─ migrations/
   ├─ versions/
   |  └─...
   ├─ env.py
   └─ script.py.mako
alembic.ini
Dockerfile
docker-compose.yml
requirements.txt
README.md
```