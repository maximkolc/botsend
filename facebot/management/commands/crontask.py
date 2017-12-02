import datetime
from django.core.management.base import BaseCommand, CommandError
from facebot.models import Task
import telebot
from telebot import types
from  urllib.request import urlopen 
from .utils.utils import YandexHelp
from .utils.getkeyboard import *
import requests
import logging
logging.basicConfig(filename="/home/maxim/sample.log",format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
logging.info("Informational message CRONTASK.PY")
logging.error("An error has happened! CRONTASK.PY")

class Command(BaseCommand):
    help = 'Export data to remote server'

    def add_arguments(self, parser):
        parser.add_argument('task_id', nargs=1, type=int)

    def handle(self, *args, **options):
        mytask = Task.objects.get(pk=options['task_id'][0])
        folder = mytask.catalog.name
        filetypes = []
        #filetypes.append(mytask.filetypesforload.ftype)
        for ft in mytask.filetypesforload.all():
            filetypes.append(ft.ftype)
        logging.info('Количество файлов для загрузки:'+ str(mytask.numfileforpub))
        logging.info(filetypes)
        dt = 'AQAAAAAiLO4jAASpE4hjRA8whkHXq9L0eQgRAKs'
        mt = 'AQAAAAAGNdiUAASpE10gPn6ctEaLhCrjmGv4sqo'
        helper = YandexHelp(token = dt)
        logging.info(helper)
        listfile = helper.getListFle(folder,filetypes,numsfile=mytask.numfileforpub)
        logging.info('файлы для загрузки '+' '.join(listfile))
        links = helper.getLinkFile(folder, listfile)
        tb = telebot.TeleBot(mytask.bottoken.bottoken)
        logging.info('бот создан')
        chanel = mytask.chanelforpublic.chanelname
        for link in links:
            url = urlopen(link)
            file = url.read()
            mykeys = []
            keyboard = None
            #tb.send_video(mytask.chanelforpublic.chanelname, f,timeout=15)
            #f = None
            if len(mytask.url.all()) >0:
                for key in mytask.url.all():
                    mykeys.append(key.urlname)
                    mykeys.append(key.url)
                keyboard = GenerateKeyboard.create_keyboard(type_keyboard = 'link',keys=mykeys) 
            logging.info(keyboard)
            if 'gif' in filetypes:
                if len(mytask.url.all()) >0:
                    tb.send_video(chanel, file,caption = mytask.caption,reply_markup = keyboard,timeout=15)
                else:
                    logging.info('gif')
                    tb.send_video(chanel, file, caption = mytask.caption,timeout=15)
            
            elif 'jpg' in filetypes or 'png' in filetypes:
                if len(mytask.url.all()) >0:
                    tb.send_photo(chanel, file,caption = mytask.caption,reply_markup = keyboard,timeout=15)
                else:
                    logging.info('jpg')
                    tb.send_photo(chanel,file,caption = mytask.caption,timeout=15)
            elif 'txt' in filetypes:
                if len(mytask.url.all()) >0:
                    tb.send_message(chanel, file.read(),caption = mytask.caption,parse_mode='Markdown',reply_markup = keyboard,timeout=15)
                else:
                    logging.info('txt')
                    tb.send_message(chanel, file,caption = mytask.caption,parse_mode='Markdown',timeout=15)
            
       