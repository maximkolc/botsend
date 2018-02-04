from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django import forms
import requests

#from .forms import RenewTaskForm
# Опять же, спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
import os
import subprocess
from django.contrib.auth.mixins import LoginRequiredMixin
# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.

from django.core import management
from .models import Task, Chanels, SourcesData, Urls, MyBot,Shedule


def logs(requests):
    '''
    Функция для работы с логами просмотр списка логов и детали лога
    '''
    t =os.getcwd()
    list_logs = os.listdir(path='logs')
    return render(
        requests,
        'facebot/logos.html',
        context={'list_logs':list_logs,'t':t},
    ) 
def log_detail(requests, log_file):
    '''
    Функция для работы с логами, детальный просмотр лога
    '''
    input = open('logs/'+log_file, 'r')
    res = input.readlines()
    return render(
        requests,
        'facebot/log.html',
        context={'res':res},
    )       

def test_run(requests,id_task):
    """
    Функция отвечающая за запуск джаного задачи кнопкой в списке задач, для теста!
    """
    com1 = '/home/maxim/work/botenv2/bin/python  /home/maxim/work/botsend/manage.py crontask '
    com2 = 'python3  ~/botsend/manage.py crontask '
    management.call_command("crontask", id_task)
    '''
    отправка email письма!!!
    from django.core.mail import send_mail
    from django.conf import settings
    send_mail('Тема', 'Тело письма', settings.EMAIL_HOST_USER, ['maximkolc@gmail.com'])
    '''
    return HttpResponseRedirect(reverse('tasks'))

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    if request.user.is_authenticated():
        # Генерация "количеств" некоторых главных объектов
        num_tasks=Task.objects.filter(created_by=request.user).count() #количество задач
        num_chanels=Chanels.objects.filter(created_by=request.user).count() #количество канала
        num_source = SourcesData.objects.filter(created_by=request.user).count() #количество источников
        num_bots = MyBot.objects.filter(created_by=request.user).count() #количество ботов
        # Отрисовка HTML-шаблона index.html с данными внутри 
        # переменной контекста context
        return render(
            request,
            'index.html',
            context={'num_tasks':num_tasks,'num_chanels':num_chanels, 'num_source':num_source,'num_bots':num_bots},)
    else:
        return HttpResponseRedirect(reverse('login'))

def getfolder(request,pk):
    '''
    Функция отдающая в ответ список каталогов с количествов
    файлов в них, на яндекс диске, ответ в формате json
    '''
    from django.core import serializers
    import json
    if request.user.is_authenticated():
        disk = get_object_or_404(SourcesData, id = pk)
        #disk = SourcesData.objects.get(id=pk)
        token  = disk.token
        folder = []
        base_url = "https://cloud-api.yandex.net:443/v1/disk"
        url = base_url + "/resources"
        base_headers = {
                "Accept": "application/json",
                "Authorization": "OAuth " + token,
                "Host": "cloud-api.yandex.net"
            }
        payload = {'path': '/','fields':'_embedded.items.name, _embedded.items.type'}
        r = requests.get(url, headers=base_headers, params=payload)
        res = r.json()
        folder = []
        numsF =[]
        for items in res['_embedded']['items']:
            if items['type'] == 'dir' and items['name']!=' ':
                folder.append(items['name'])
                numsF.append(getNumsF(0, tok=token, folder = items['name']))
        res = dict(zip(folder, numsF))
        return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json")
    else:
        return HttpResponseRedirect(reverse('login'))

def getNumsF(n, **kwargs):
    '''вспомогательная функция для функции получения списка списка каталоговы
       подсчитывает количество файлов в каталоге на яндекс диске
    '''
    sum =0
    token = kwargs['tok']
    fol = kwargs['folder']
    base_headers = {
    "Accept": "application/json",
    "Authorization": "OAuth " + token,
    "Host": "cloud-api.yandex.net"
    }
    base_url = "https://cloud-api.yandex.net:443/v1/disk"
    url = base_url + "/resources"
    payload = {'path': fol,'fields':'_embedded.items.name, _embedded.items.type','offset':n}
    r = requests.get(url, headers=base_headers,params=payload)
    nums = len(r.json()['_embedded']['items'])
    if nums < 20:
        return sum + nums
    else:
        k = payload['offset']+nums
        #sum = nums
        return nums + getNumsF(k, tok = token, folder = fol)



def gettoken(request):
    if request.method == 'GET':
        pcode = request.GET['code']
    base_headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        
        'Authorization':'basic OGM5NGFkOWQ5NzU3NGRmNDhmNzdjOTkxNGZlOWIyMGQ6NDk1NzkyYjhjYTA4NDM5NGE5OTljNGMyODg3ZTA5YmE='
        }
    payload = {'grant_type':'authorization_code','code': pcode}
    url = 'https://oauth.yandex.ru/token'
    r = requests.post(url, headers= base_headers,data={'grant_type':'authorization_code','code': pcode})
    json_dict = r.json()
    token_ya = json_dict['access_token']
    request.session["token"] = token_ya
    return HttpResponseRedirect(reverse('sources_create'))
  
