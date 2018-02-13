import telebot
from telebot import types
from botsend.celery import app
from datetime import timedelta
from datetime import datetime
import time
import facebot.models 
from django.utils import timezone
from  urllib.request import urlopen 
from celery.utils.log import get_task_logger

logger = get_task_logger('__name__')
@app.task()
def send_once(id_task):
    task = facebot.models.OnceTask.objects.get(id=id_task)
    tb = telebot.TeleBot(task.bottoken.bottoken)
    try:
        tb.send_photo('@cool_chanel', task.imgs,caption=task.text)
    except (ConnectionError) as exc:
        raise self.retry(exc=exc)


