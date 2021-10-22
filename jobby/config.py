import psycopg2, os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '7c6b7967-dcba-4796-a261-f36b028144e3'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:WulIgtM5zk@localhost/jobby"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WHOOSH_BASE = 'whoosh'
    MAIL_SERVER = "mail server"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "email"
    MAIL_PASSWORD = "password"
