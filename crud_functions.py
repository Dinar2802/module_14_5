import sqlite3


def initiate_db():
    connection = sqlite3.connect('database_product.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')
    for i in range(4):
        cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                       (f'продукт(new){i + 1}', f'описание(new){i + 1}', f'{(i + 1) * 100}'))

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')

    connection.commit()
    connection.close()


# initiate_db()


def add_user(username, email, age):
    connection = sqlite3.connect('database_product.db')
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)
    """, (username, email, age, 1000))
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect('database_product.db')
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    connection.close()
    return user is not None
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('database_product.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.close()
    return products
