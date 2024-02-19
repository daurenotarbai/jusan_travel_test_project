# Jusan Travel Test Task Project

Auth Service

## Начало работы

Убедитесь, что у вас установлены git, docker, docker-compose

### Предварительные требования
```
git clone https://your-repository-url.git
```
```
cd jusan_travel_test_project
```
Запустите проект
```
docker-compose up --build up -d
```
Заходите в контейнер
```
docker exec -it  jusan_travel_test_project_web_1 bash
```

Заходите в migration файл
```
cd app/migrations
```
Выполняйте миграцию
```
aerich upgrade
```

Документация на swagger доступно в 0.0.0.0:8000/docs

## Используемые технологии

* [FastAPI](https://fastapi.tiangolo.com/) - Веб-фреймворк, используемый для создания API
* [Tortoise ORM](https://tortoise-orm.readthedocs.io/en/latest/) - ORM для работы с базой данных
* [Docker](https://www.docker.com/) - Используется для контейнеризации приложения
* [Pydantic](https://pydantic-docs.helpmanual.io/) - Используется для валидации данных