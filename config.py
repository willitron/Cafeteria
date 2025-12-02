import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-desarrollo-2024'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cafeteria.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False