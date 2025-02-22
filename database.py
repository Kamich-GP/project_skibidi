# Работа с базой данных
import sqlite3


# Подключение к БД
connection = sqlite3.connect('delivery.db', check_same_thread=False)
# Python + SQL
sql = connection.cursor()


# Создание таблиц
sql.execute('CREATE TABLE IF NOT EXISTS users '
            '(user_id INTEGER, user_name TEXT, user_num TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS products '
            '(pr_id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'pr_name TEXT, pr_des TEXT, pr_count INTEGER, '
            'pr_price REAL, pr_photo TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS cart '
            '(user_id INTEGER, user_pr TEXT, user_pr_count INTEGER);')



## Методы пользователя ##
# Регистрация
def register(user_id, user_name, user_num):
    sql.execute('INSERT INTO users VALUES (?, ?, ?);',
                (user_id, user_name, user_num))
    # Фиксируем изменения
    connection.commit()


# Проверка на наличие пользователя в БД
def check_user(user_id):
    if sql.execute('SELECT * FROM users WHERE user_id=?;', (user_id,)).fetchone():
        return True
    else:
        return False
