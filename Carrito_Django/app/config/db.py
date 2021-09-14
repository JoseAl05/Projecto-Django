import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POSTGRESQL = {
    'default' :{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'carrito',
        'USER': 'postgres',
        'PASSWORD': 'jpal0598',
        'HOST': 'localhost',
        'POST': '5432',
    }
}