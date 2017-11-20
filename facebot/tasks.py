import telebot
from telebot import types
from botsend.celery import app
from datetime import timedelta
from datetime import datetime
import time
import facebot.models 
from django.utils import timezone
from  urllib.request import urlopen 
from .utils.utils import YandexHelp
@app.task
def send_mess(id_task):
    mytask = facebot.models.Task.objects.get(id=id_task)
    folder = mytask.catalog.name
    filetypes = mytask.filetypesforload
    helper = YandexHelp(token = "AQAAAAAGNdiUAASpE10gPn6ctEaLhCrjmGv4sqo")
    
    
    time.sleep((mytask.time_run-timezone.now()).seconds)
   
    listfile = helper.getListFle(folder,filetypes,numsfile=1)
    links = helper.getLinkFile(folder, listfile)
    tb = telebot.TeleBot(mytask.bottoken.bottoken)
    for link in links:
        url = urlopen(link)    
        f = url.read()
        tb.send_video(mytask.chanelforpublic.chanelname, f)
        f = None
    #tb.send_message(mytask.chanelforpublic.chanelname, "Сообщение отправлено "+ str(mytask.time_run))
    mytask.time_run = mytask.time_run+mytask.time_period
    mytask.save()
   

