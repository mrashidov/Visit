Places Web site powered by Django 2.0
--------------------------------------------------------

Требования:
- Python 3
- MariaDB/MySQL 
- bower
    - nodejs

Установка 
1. Установим все программы, необходимые для работы проекта
Windows:
    1. Скачать пакет с Python 3 с официального сайта:
        - https://www.python.org/download/releases/3.0/
    2. Установить согласно инструкции
    3. Скачать и установить MySQL/MariaDB
    4. Скачать и установить NodeJS
    5. >npm install -g bower
2. Подготовка к запуску
    1. Запустить MySQL/MariaDB сервер
    2. >mysql -u root -p
    3. Ввести пароль (если запуск первый, то он пустой)
    4. Создать пользователя:
        >CREATE USER p_admin IDENTIFIED BY 'password';
    5. Создать базу данных:
        >CREATE DATABASE p_places_db;
    6. Предоставим пользователю p_admin эксклюзивные привелегии на БД p_places_db
        >grant all privileges on p_placed_db.* to p_admin;
        >FLUSH PRIVILEGES;
    7. Перейти к папке с проектом и открыть ее.
    8. Установить необходимые пакеты для проекта:
        >python3 install -r requirements
    9. Запустить миграции для создания связи моделей проекта с базой данных
        >python3 manage.py makemigrations;
        >python3 manage.py migrate;
    10. Запустить bower для установки необходимых пакетов (bootstrap. nodejs):
        >python3 manage.py bower install;
    11. Создать суперпользователя сервера:
        >python3 manage.py createsuperuser
    11. Запустить проект: 
        >python3 manage.py runserver;
    12. Войти в административную страницу:
        >localhost:8000/admin
    13. Использовав пароль и логин суперпользователя, войдите в часть сайта, доступную персоналу
    14. Заполните базу данных значениями.
    15. Запустите тестовый сервер:
        >python3 manage.py runserver

Вопросы и помощь предоставляются мной. 
