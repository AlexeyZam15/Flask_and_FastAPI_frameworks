"""Соединение с базой данных mydatabase.db из папки instance и вывод всех записей"""

import sqlite3

conn = sqlite3.connect('instance/mydatabase.db')
cur = conn.cursor()
cur.execute('SELECT * FROM user')
print(cur.fetchall())
conn.close()
