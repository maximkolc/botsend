from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse as rv
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django import forms
import requests
from django.shortcuts import redirect, reverse, Http404
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
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
import json
from django.core import management
from .models import Task, Chanels, SourcesData, Urls, MyBot,Shedule, ImageUpload
from .forms import CustomUserCreationForm, ImageUploadForm
from facebot import helpers
from .models import Profile
from datetime import date
import telebot
def register(request):
    #получаем ip адресс пользователя при регистрации
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            # send email verification now
            activation_key = helpers.generate_activation_key(username=request.POST['username'])
            subject = "Подтверждения аккаунта"
            message = '''\n Для подтверждения аккаунта переидите по этой ссылке \n\n{0}://{1}/facebot/activate/account/?key={2}
                        '''.format(request.scheme, request.get_host(), activation_key)            
            error = False
            try:
                #send_mail(subject, message, settings.EMAIL_HOST_USER, [request.POST['email']])
                tb = telebot.TeleBot('460229690:AAGfrgxIU1Hh6dBAv0LoYsAWd4YUF7cvLHQ')
                mes = '''
                **Запрос на регистрацию нового пользователя:** 
                1. *username*: {0}
                2. *email*: {1}
                3. *логин в телеграмме*: {2}
                4. *ссылка для активации аккаунта*: {3},
                '''.format(request.POST['username'],request.POST['email'],request.POST['telega'],message)

                tb.send_message('@cool_chanel',mes, parse_mode='Markdown')
                
            except:
                error = True
                print ("!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!!!!11") 
            if not error:
                u = User.objects.create_user(
                    request.POST['username'],
                    request.POST['email'],
                    request.POST['password1'],
                    is_active = 0
                    )
                profile = Profile()
                profile.activation_key = activation_key
                profile.user = u
                profile.ip_adress = ip
                profile.telegramm = request.POST['telega']
                profile.datetowork = date.today()
                profile.save()
            return HttpResponseRedirect(rv('login'))
    else:
        f = CustomUserCreationForm()
    return render(request, 'register.html', {'form': f})

def activate_account(request):
    key = request.GET['key']
    if not key:
        raise Http404()

    r = get_object_or_404(Profile, activation_key=key, email_validated=False)
    r.user.is_active = True
    r.user.save()
    r.email_validated = True
    r.save()

    return render(request, 'activate.html')

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
    task = Task.objects.get(id=id_task)
    
    messages.info(requests, 'Задача '+task.taskname+" "+task.status)
    return HttpResponseRedirect(rv('tasks'))

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
        return HttpResponseRedirect(rv('login'))

def getfolder(request,pk):
    '''
    Функция отдающая в ответ список каталогов с количествов
    файлов в них, на яндекс диске, ответ в формате json
    '''
    
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
        return HttpResponseRedirect(rv('login'))

def getNumsF(n, **kwargs):
    '''вспомогательная функция для функции получения списка списка каталоговы
       подсчитывает количество файлов в каталоге на яндекс диске
    '''
    token = kwargs['tok']
    fol = kwargs['folder']
    base_headers = {
    "Accept": "application/json",
    "Authorization": "OAuth " + token,
    "Host": "cloud-api.yandex.net"
    }
    base_url = "https://cloud-api.yandex.net:443/v1/disk"
    url = base_url + "/resources"
    payload = {'path': fol,'fields':'_embedded.total'} #items.name, _embedded.items.type','offset':n}
    r = requests.get(url, headers=base_headers,params=payload)
    nums = r.json()['_embedded']['total'] #['items'])
    #if nums < 20:
    #    return sum + nums
    #else:
    #    k = payload['offset']+nums
    #    #sum = nums
    #    return nums + getNumsF(k, tok = token, folder = fol)
    return nums



def gettoken(request):
    if request.method == 'GET':
        pcode = request.GET['code']
    base_headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        
        'Authorization':'basic N2I1NjBiNTY1MjMyNGYxODlmZmU5ZTIzMGIwNTI0Mjk6YjI1NzU2NWUxN2ViNDU3NThhZWNlMjgyYzNjNjk4ODU=' 
         #OGM5NGFkOWQ5NzU3NGRmNDhmNzdjOTkxNGZlOWIyMGQ6NDk1NzkyYjhjYTA4NDM5NGE5OTljNGMyODg3ZTA5YmE='
        }
    payload = {'grant_type':'authorization_code','code': pcode}
    url = 'https://oauth.yandex.ru/token'
    r = requests.post(url, headers= base_headers,data={'grant_type':'authorization_code','code': pcode})
    json_dict = r.json()
    token_ya = json_dict['access_token']
    request.session["token"] = token_ya
    return HttpResponseRedirect(rv('sources_create'))
  
def profile(request):
    try:
        p = Profile.objects.get(user=request.user)
        u = User.objects.get(pk=request.user.id) 
    except Profile.DoesNotExist:
        raise Http404("Poll does not exist")
    return render(request, 'facebot/profile.html', {'user': u, 'prorile':p })

def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = ImageUpload() #.objects.get(pk=course_id))
            m.model_pic = form.cleaned_data['image']
            m.save()
            data = {'is_valid': True, 'name': m.model_pic.name, 'url': m.model_pic.url}
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")

        else:
            data = {'is_valid': False}
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")