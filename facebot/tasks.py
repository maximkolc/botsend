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
import json

logger = get_task_logger('__name__')
@app.task()
def send_once(id_task):
    task = facebot.models.OnceTask.objects.get(id=id_task)
    tb = telebot.TeleBot(task.bottoken.bottoken)
    try:
        message = tb.send_message('@cool_chanel',task.text,parse_mode='Markdown') #task.imgs,caption=task.text)
    except:
        raise retry()
    #json_data = json.dumps(resp) 
    #parsed_json = resp.de_json()
    #print("message_id: "+str(resp.message_id)+str(resp.chat))
    time.sleep((task.del_date - task.run_date).total_seconds())
    tb.delete_message(message.chat.id, message.message_id)

