import mysql.connector
from flask import g


class MySQL:
    def __init__(self, app):
        self.app = app # Сохраняем экземпляр приложения Flask, переданный в конструктор класса
        self.app.teardown_appcontext(self.close_connection) # Регистрируем функцию close_connection 
        # как функцию для закрытия соединения с базой данных при завершении работы приложения
    
    def config(self):
        return {
            "user": self.app.config['MYSQL_USER'], 
            "password": self.app.config['MYSQL_PASSWORD'],
            "host": self.app.config['MYSQL_HOST'],
            "database": self.app.config['MYSQL_DATABASE']
        }

    def close_connection(self, e=None):
        db = g.pop('db', None) # Получаем объект базы данных 'db' из контекста приложения Flask и удаляем его из контекста

        if db is not None: # Если объект базы данных существует
            db.close() # закрываем соединение с базой данных

    def connection(self):
        if 'db' not in g: # Проверяем, есть ли объект подключения к базе данных в контексте приложения Flask
            g.db = mysql.connector.connect(**self.config()) # Если объекта нет, 
            # создаем новый объект подключения к базе данных с помощью параметров настроек, переданных в конфигурацию
        return g.db # Возвращаем объект подключения к базе данных из контекста приложения Flask