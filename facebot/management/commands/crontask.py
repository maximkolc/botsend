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
import random
from facebot.models import MessageReaction, Profile, Messages
import json
import time
#logging.basicConfig(filename="logs/crontask_logo.log",format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

class Command(BaseCommand):
    help = 'Export data to remote server'
    
    def add_arguments(self, parser):
        parser.add_argument('task_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        from django.conf import settings
        for task_id in options['task_ids']:
            #получение всех данных для задачи
            mytask = Task.objects.get(pk=task_id)
            folder = mytask.catalog_ajax
            filetypes = []
            for ft in mytask.filetypesforload.all():
                t = ft.ftype.split(',')
                filetypes.extend(t)
            nums_file_load = 0
            if mytask.numfileforpub_random == True:
                nums_file_load = random.randint(mytask.num_file_min, mytask.num_file_max)
            else:
                nums_file_load = mytask.numfileforpub
            chanel = mytask.chanelforpublic.chanelname
            yande_token = mytask.sourcefordownload.token
            tb = telebot.TeleBot(mytask.bottoken.bottoken)
            helper = YandexHelp(token = yande_token)
            
            #настройка логера
            file_name_log = mytask.created_by.username.replace(' ', '') + "_log.log"
            logger = logging.getLogger("run_task")
            logger.setLevel(logging.INFO)
            fh = logging.FileHandler(settings.BASE_DIR+"/logs/"+file_name_log)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            
            # получения пользователя, который создал задачу
            user = Profile.objects.get(user = mytask.created_by)
            # проверка даты, до которой пользователь может выполнять задачи
            if datetime.datetime.now() < user.datetowork.replace(tzinfo=None):
                logger.info("Начало выполнение задачи - "+mytask.taskname)
                logger.info('Бот '+str(mytask.bottoken)+' создан')
                logger.info("Каталог c файлами для "+mytask.taskname +": "+folder)
                logger.info('Количество файлов для загрузки:'+ str(nums_file_load))
                logger.info('Типы загружаемых файлов '+' '.join(filetypes))        
                logger.info('Канал для публикации: '+chanel)
                #print("11111111111111111111111111111111111111")
                #Получение списка файлов для загрузки
                listfile = helper.getListFle2(folder,filetypes,numsfile=nums_file_load,log=file_name_log)
                logger.info('файлы для загрузки '+' '.join(listfile))
                links = helper.getLinkFile(folder, listfile)
                logger.info('Полученные ссылки для загрузки файлов: '+' '.join(links))
                
                # добавление клавиатуры, то есть кнопок с лайками под постами
                mykeys = []
                keyboard = None
                #if len(mytask.url.all()) >0:
                #    for key in mytask.url.all():
                #mykeys.append("да")
                #mykeys.append("нет")
                #keyboard = GenerateKeyboard.create_keyboard(type_keyboard = 'inline',keys=mykeys) 
                #keyboard = types.InlineKeyboardMarkup()
                #callback_button = types.InlineKeyboardButton(text="like", callback_data="like")
                #keyboard.add(callback_button)
                #logger.info("Кнопки под постом добавленны: "+str(keyboard))
                if len(mytask.url.all()) <= 0:
                    logger.info('Кнопки под постом отсутствуют')
                messages = [] #для сбора информации об отправленных файлах
                # скачивание файлов и т.д. для отправки в телеграмм
                #start = time.time()
                #i = 0
                for link,filename in zip(links, listfile):
                    url = urlopen(link)
                    file = url.read()
                    #i = i+1
                    if filename.split('.')[1] in ['gif','mp4','avi']:
                        logger.info('Отпрака файла '+filename+' как видео')
                        if len(mytask.url.all()) >0:
                            message = tb.send_video(chanel, file,caption = mytask.caption,reply_markup = keyboard,timeout=15)
                        else:
                            message = tb.send_video(chanel, file, caption = mytask.caption,timeout=15)
                        messages.append(message)
                            
                    elif filename.split('.')[1] in ['jpeg','jpg','png']:
                        logger.info('Отпрака файла: '+filename+' как картинку')
                        if len(mytask.url.all()) >0:
                            message = tb.send_photo(chanel, file,caption = mytask.caption,reply_markup = keyboard)
                        else:
                            message = tb.send_photo(chanel,file,caption = mytask.caption)
                        messages.append(message)
                    elif filename.split('.')[1] in ['txt']:
                        logger.info('Отпрака файла: '+filename+' как текст')
                        if len(mytask.url.all()) >0:
                            message = tb.send_message(chanel, file.read(),caption = mytask.caption,parse_mode='Markdown',reply_markup = keyboard)
                        else:
                            message = tb.send_message(chanel, file,parse_mode='Markdown')
                        messages.append(message)
                    #запись в бд информации об отправленном сообщении
                    for message in messages:
                        chat_id = str(message.chat.id)
                        message_id = str(message.message_id)
                        m = MessageReaction(chat_id = chat_id, 
                                            message_id = message_id, 
                                            like_count = 0, 
                                            dislike_count = 0,
                                            created_by = mytask.created_by,
                                            chanel_name = chanel,
                                            bottoken = mytask.bottoken.bottoken,
                                            task = mytask,
                                            created_at = datetime.datetime.now().strftime("%y-%m-%d-%H:%M"))
                        m.save()   
                # Удаление файла с диска, если отмечено соответвуещее
                if mytask.isfiledelete:
                    res = helper.remove_folder_or_file(folder,listfile)    
                    logger.info(''.join(res))
                mytask.status = "Последний раз выполнена "+str(datetime.datetime.now().strftime("%y-%m-%d-%H:%M"))
                mytask.save()
                #print("Process took: {:.2f} seconds".format(time.time() - start))
            else:
                mytask.status = "ПРООДЛИТЕ ПОДПИСКУ!"
                mytask.save()
                logger.info("Истекла подписка  - "+mytask.created_by.username)
    