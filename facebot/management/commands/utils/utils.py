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
import requests
#import logging

#token = "AQAAAAAGNdiUAASpE10gPn6ctEaLhCrjmGv4sqo"

class YandexHelp:
    def __init__(self,token):
        self.token = token
        self.client = YandexDiskRestClient(self.token)
        
    def getListFle2(self, folder,filetypes,numsfile,log):
        #повесить исключение по количеству файлов
        list = self.client.get_content_of_folder(folder).get_children()  
        #print("Всего файлов в каталоге: - "+ str(len(list)))
        new_list = []
        list_for_load=[]
        for key in list:
            ext = key.name.split('.')[1]
            if ext.lower() in filetypes:
                new_list.append(key.name)  
        #logger.info("Из них файлов удовлетворящюх требованиям: - "+ str(len(new_list)))
        random.shuffle(new_list)
        if(numsfile>1):
            for i in range(numsfile):
                list_for_load.append(new_list[i])
        else:
            list_for_load.append(new_list[1])
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
    
    def get_links(self,dir, filetypes, num_file):
        base_url = "https://cloud-api.yandex.net:443/v1/disk"
        base_headers = {
            "Accept": "application/json",
            "Authorization": "OAuth " + self.token,
            "Host": "cloud-api.yandex.net"
        }
        url = base_url + "/resources"
        payload = {'path': dir, 'fields':' _embedded.total'}
        r = requests.get(url, headers=base_headers,params=payload)
        total = r.json()['_embedded']['total']
        links = []
        files = [] 
        offset = total - 1
        i =0 
        while i != num_file: 
            payload = {'path': 'humor', 'fields':'_embedded.items.name, _embedded.items.file', 'offset':offset}
            response = requests.get(url,headers = base_headers, params=payload)
            file = response.json()
            ext = file['_embedded']['items'][0]['name'].split('.')[1]
            if ext.lower() in filetypes:
                links.append(file['_embedded']['items'][0]['file'])
                files.append(file['_embedded']['items'][0]['name'])
            offset = offset - 1
            i = i+1
        return zip (links,files) 





