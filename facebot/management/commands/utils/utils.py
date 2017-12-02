# Методы оказывающие помощь в получении сообщения
'''
1. Метод для получения списка файлов с диска (каталог на диске), 
2. Метод для загрузки нужных файлов (расширение, список файлов(ссылок))

'''

import random
import string
import sys
import re
from .src.YandexDiskException import YandexDiskException
from .src.YandexDiskRestClient import YandexDiskRestClient
from .src.YandexDiskRestClient import Directory
import random

#token = "AQAAAAAGNdiUAASpE10gPn6ctEaLhCrjmGv4sqo"

class YandexHelp:
    def __init__(self,token):
        self.token = token
        self.client = YandexDiskRestClient(self.token)
        
    def getListFle(self, folder,filetypes,numsfile):
        list = self.client.get_content_of_folder(folder).get_children()  
        new_list = []
        list_for_load=[]
        for key in list:
            new_list.append(key.name)  
        ftypes_r = ''+'|'.join(filetypes) #filetypes - список!!!!!!
        new_list = re.findall(r'\w+.(?:'+ftypes_r+')',''+' '.join(new_list))
        random.shuffle(new_list)
        for i in range(numsfile):
            list_for_load.append(new_list[i])
        return list_for_load

    def getLinkFile(self, folder, list_for_load):
        links = []
        for filename in list_for_load:
            link = self.client.get_download_link_to_file('/'+folder+'/'+filename)
            links.append(link['href'])
        return links
    
        





