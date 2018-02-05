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
#import logging

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

    def getListFle2(self, folder,filetypes,numsfile,log):
        list = self.client.get_content_of_folder(folder).get_children()  
        #logger.info("Всего файлов в каталоге: - "+ str(len(list)))
        new_list = []
        list_for_load=[]
        for key in list:
            ext = key.name.split('.')[1]
            if ext.lower() in filetypes:
                new_list.append(key.name)  
        #logger.info("Из них файлов удовлетворящюх требованиям: - "+ str(len(new_list)))
        random.shuffle(new_list)
        for i in range(numsfile):
            list_for_load.append(new_list[i])
        return list_for_load
    
    def remove_folder_or_file(self,folder, listfiles):
        result = []
        try:
            for filename in listfiles:
                self.client.remove_folder_or_file('/'+folder+'/'+filename)
                result.append("The file " + filename + " was successfully removed.")
            return result
        except YandexDiskException as exp:
            result.append(exp)
            return result
            #sys.exit(1)

    def getLinkFile(self, folder, list_for_load):
        links = []
        for filename in list_for_load:
            #print (filename)
            link = self.client.get_download_link_to_file('/'+folder+'/'+filename)
            links.append(link['href'])
        return links
    
    def get_disk_metadata(self):
        try:
            disk = self.client.get_disk_metadata()
            result = "всего места на диске = " + str(disk.total_space)+"\n"
            result = result+"занято места на диске = " + str(disk.used_space)
        except YandexDiskException as exp:
            result = str(exp)
            #sys.exit(1)
            return result
        return result
    def get_list_of_all_files(self):
        try:
            files = self.client.get_list_of_all_files()
            result = "There are " + str(len(files)) + " files in this Yandex.Disk"
        except YandexDiskException as exp:
            result = str(exp)
            #sys.exit(1)
            return result
        return result





