import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = [
     '127.0.0.1',
]
STATIC_ROOT = '/home/maxim/static'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DEBUG = True
com2 = '/home/maxim/work/botenv2/bin/python  /home/maxim/work/botsend/manage.py crontask '

