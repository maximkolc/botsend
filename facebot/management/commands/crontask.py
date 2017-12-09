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
#logging.basicConfig(filename="logs/crontask_logo.log",format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

class Command(BaseCommand):
    help = 'Export data to remote server'

    def add_arguments(self, parser):
        parser.add_argument('task_id', nargs=1, type=int)

    def handle(self, *args, **options):
        mytask = Task.objects.get(pk=options['task_id'][0])
        file_name_log = mytask.taskname + "_log.log"
        #logging.basicConfig(filename="logs/"+file_name_log,format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
        logger = logging.getLogger("run_task")
        logger.setLevel(logging.INFO)
        # create the logging file handler
        fh = logging.FileHandler("logs/"+file_name_log)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        # add handler to logger object
        logger.addHandler(fh)
        logger.info("Начало выполнение задачи - "+mytask.taskname)
        folder = mytask.catalog.name
        logger.info("Каталог c файлами для "+mytask.taskname +": "+folder)
        filetypes = []
        for ft in mytask.filetypesforload.all():
            t = ft.ftype.split(',')
            filetypes.extend(t)
            print(filetypes)
        logger.info('Количество файлов для загрузки:'+ str(mytask.numfileforpub))
        logger.info('Типы загружаемых файлов '+' '.join(filetypes))
        dt = mytask.sourcefordownload.token
        test = 'AQAAAAAiLO4jAASpE0JmHehiVkahtwsJmy1J9fc'
        helper = YandexHelp(token = dt)
        #-----------
        logger.info("Данные о диске:\n "+ helper.get_disk_metadata())
        #helper.get_list_of_all_files()
        #-----------
        logger.info("Получение списка файлов для загрузки")
        listfile = helper.getListFle2(folder,filetypes,numsfile=mytask.numfileforpub,log=file_name_log)
        logger.info('файлы для загрузки '+' '.join(listfile))
        links = helper.getLinkFile(folder, listfile)
        logger.info('Полученные ссылки для загрузки файлов: '+' '.join(links))
        tb = telebot.TeleBot(mytask.bottoken.bottoken)
        logger.info('Бот '+str(mytask.bottoken)+' создан')
        chanel = mytask.chanelforpublic.chanelname
        logger.info('Канал для публикации: '+chanel)
        #for x, y in zip(key_dict, value_dict):
        #dict_out[x] = y
        mykeys = []
        keyboard = None
        if len(mytask.url.all()) >0:
            for key in mytask.url.all():
                mykeys.append(key.urlname)
                mykeys.append(key.url)
                keyboard = GenerateKeyboard.create_keyboard(type_keyboard = 'link',keys=mykeys) 
            logger.info("Кнопки под постом добавленны: "+str(keyboard))
        if len(mytask.url.all()) <= 0:
            logger.info('Кнопки под постом отсутствуют')
        for link,filename in zip(links, listfile):
            url = urlopen(link)
            file = url.read()
            if filename.split('.')[1] in ['gif','mp4','avi']:
                logger.info('Отпрака файла '+filename+' как видео')
                if len(mytask.url.all()) >0:
                    tb.send_video(chanel, file,caption = mytask.caption,reply_markup = keyboard,timeout=15)
                else:
                    tb.send_video(chanel, file, caption = mytask.caption,timeout=15)
            
            elif filename.split('.')[1] in ['jpeg','jpg','png']:
                logger.info('Отпрака файла: '+filename+' как картинку')
                if len(mytask.url.all()) >0:
                    tb.send_photo(chanel, file,caption = mytask.caption,reply_markup = keyboard)
                else:
                    tb.send_photo(chanel,file,caption = mytask.caption)
            elif filename.split('.')[1] in ['txt']:
                logger.info('Отпрака файла: '+filename+' как текст')
                if len(mytask.url.all()) >0:
                    tb.send_message(chanel, file.read(),caption = mytask.caption,parse_mode='Markdown',reply_markup = keyboard)
                else:
                    tb.send_message(chanel, file,parse_mode='Markdown')
        res = helper.remove_folder_or_file(folder,listfile)    
        logger.info(''.join(res))
