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
    chanels = []
    messages = []
    for ft in task.chanelforpublic.all():
        chanels.append(ft.chanelname)
    tb = telebot.TeleBot(task.bottoken.bottoken)
    try:
        for chanel in chanels:
            print (chanel)
            task = facebot.models.OnceTask.objects.get(id=id_task)
            #message = tb.send_photo(chanel,task.imgs,caption=task.text)
            message = tb.send_message(chanel,task.text, parse_mode='Markdown')
            time.sleep(5)
            messages.append(message)
        facebot.models.OnceTask.objects.filter(id=id_task).update(status = "Ожидает удаления "+ str(task.del_date))
        #task.update(status = "Ожидает удаления "+ str(task.del_date))
    except:
        #task.update(status = "Задача не выполнена")
        facebot.models.OnceTask.objects.filter(id=id_task).update(status = "Задача не выполнена")
    #json_data = json.dumps(resp) 
    #parsed_json = resp.de_json()
    #print("message_id: "+str(resp.message_id)+str(resp.chat))
    time.sleep((task.del_date - task.run_date).total_seconds())
    try:
        for message in messages:
            tb.delete_message(message.chat.id, message.message_id)
        #task.update(status = "Удалено")
        facebot.models.OnceTask.objects.filter(id=id_task).update(status = "Удалено")
    except:
        #task.update(status = "Ошибка, не удалось удалить сообщение")
        facebot.models.OnceTask.objects.filter(id=id_task).update(status = "Задача не выполнена")

@app.task()
def delete_message(id_message):
    message = facebot.models.MessageReaction.objects.get(id=id_message)
    s = requests.Session()
    s.get('https://api.telegram.org/bot{0}/deletemessage?message_id={1}&chat_id={2}'.format(
        token, 
        message.message_id, 
        message.chat.id))
    chanels = []
    messages = []
    for ft in task.chanelforpublic.all():
        chanels.append(ft.chanelname)
    tb = telebot.TeleBot(task.bottoken.bottoken)
    try:
        for chanel in chanels:
            print (chanel)
            task = facebot.models.OnceTask.objects.get(id=id_task)
            #message = tb.send_photo(chanel,task.imgs,caption=task.text)
            message = tb.send_message(chanel,task.text, parse_mode='Markdown')
            time.sleep(5)
            messages.append(message)
        facebot.models.OnceTask.objects.filter(id=id_task).update(status = "Ожидает удаления "+ str(task.del_date))
        #task.update(status = "Ожидает удаления "+ str(task.del_date))
    except:
        #task.update(status = "Задача не выполнена")
        facebot.models.OnceTask.objects.filter(id=id_task).update(status = "Задача не выполнена")
    #json_data = json.dumps(resp) 
    #parsed_json = resp.de_json()
    #print("message_id: "+str(resp.message_id)+str(resp.chat))
    time.sleep((task.del_date - task.run_date).total_seconds())
    try:
        for message in messages:
            tb.delete_message(message.chat.id, message.message_id)
        #task.update(status = "Удалено")
        facebot.models.OnceTask.objects.filter(id=id_task).update(status = "Удалено")
    except:
        #task.update(status = "Ошибка, не удалось удалить сообщение")
        facebot.models.OnceTask.objects.filter(id=id_task).update(status = "Задача не выполнена")
