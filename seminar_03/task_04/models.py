"""
Создать базу данных для хранения пользователей
"""
from bcrypt import hashpw, gensalt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Хэш пароля в байтовом представлении
    password_hash = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, email={self.email})'
