from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
import datetime
from django import forms
from .forms import EditTaskForm
from django.contrib.admin import widgets 
import requests
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
#from .forms import RenewTaskForm
# Опять же, спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm
from .models import Task, Chanels, SourcesData, Urls, MyBot, Period,Shedule
from django.views import generic
from django.contrib.auth import logout
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
import os
import subprocess
# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.
from django.contrib.auth import login
import requests
class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

class RegisterFormView(FormView):
    form_class = UserCreationForm
    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)

class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect('index')

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
    from django.core import management
    management.call_command("crontask", id_task)
    return HttpResponseRedirect(reverse('tasks'))
    
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_tasks=Task.objects.all().count() #количество задач
    num_chanels=Chanels.objects.all().count() #количество канала
    num_source = SourcesData.objects.all().count() #количество источников
    num_bots = MyBot.objects.all().count() #количество ботов
    # Отрисовка HTML-шаблона index.html с данными внутри 
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_tasks':num_tasks,'num_chanels':num_chanels, 'num_source':num_source,'num_bots':num_bots},
    )

def getfolder(request,pk):
    '''
    Функция отдающая в ответ список каталогов с количествов
    файлов в них, на яндекс диске, ответ в формате json
    '''
    from django.core import serializers
    import json
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

def getNumsF(n, **kwargs):
    '''вспомогательная функция для функции получения списка списка каталоговы'''
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
  

class TaskListView(generic.ListView):
    model = Task
    
class TaskDetailView(generic.DetailView):
    model = Task

class ChanelsListView(generic.ListView):
    model = Chanels
   

class MyBotListView(generic.ListView):
    model = MyBot
     

class SourcesDataListView(generic.ListView):
    model = SourcesData

class PeriodListView(generic.ListView):
    model = Period

class SheduleListView(generic.ListView):
    model = Shedule

class UrlsListView(generic.ListView):
    model = Urls


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        labels = {
            'chanelforpublic': 'Канал куда публикуем',
            'sourcefordownload': 'Яндекс диск',
            'filetypesforload': 'Типы публикуемых файлов',
            'bottoken': 'Публикующий бот',
            'url': 'Кнопки под публикацией',
            'catalog_ajax': 'Каталог на диске'
        }
        widgets = {
            'url': forms.CheckboxSelectMultiple(attrs={'style' : 'list-style-type: none'}),
            'filetypesforload': forms.CheckboxSelectMultiple(attrs={'style' : 'list-style-type: none'}),
            'taskname': forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Введи имя'}),
            'chanelforpublic': forms.Select(attrs={'class':'form-control'}),
            'sourcefordownload': forms.Select(attrs={'class':'form-control'}),
            'catalog_ajax': forms.Select(attrs={'class':'form-control'}),
            'reactioan': forms.Select(attrs={'class':'form-control'}),
            'numfileforpub': forms.NumberInput(attrs={'class':'form-control', 'min':1}),
            'caption':forms.Textarea(attrs = {'class':'form-control', 'placeholder':'','cols': 80, 'rows': 4}),
            'bottoken': forms.Select(attrs={'class':'form-control'}),
             }
             
class TaskCreate(CreateView):
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy('tasks')

class TaskUpdate(UpdateView):
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy('tasks')
    #fields = ['first_name','last_name','date_of_birth','date_of_death']

class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')

#MyBot
class MyBotCreate(CreateView):
    model = MyBot
    fields = '__all__'
    #initial={'momentforwork':'12/10/2016',}
    success_url = reverse_lazy('bots')

class MyBotUpdate(UpdateView):
    model = MyBot
    fields = '__all__'
    success_url = reverse_lazy('bots')
    #fields = ['first_name','last_name','date_of_birth','date_of_death']

class MyBotDelete(DeleteView):
    model = MyBot
    success_url = reverse_lazy('bots')


class ChanelsCreate(CreateView):
    model = Chanels
    fields = '__all__'
    #initial={'momentforwork':'12/10/2016',}
    success_url = reverse_lazy('chanels')

class ChanelsUpdate(UpdateView):
    model = Chanels
    fields = '__all__'
    success_url = reverse_lazy('chanels')
    #fields = ['first_name','last_name','date_of_birth','date_of_death']

class ChanelsDelete(DeleteView):
    model = Chanels
    success_url = reverse_lazy('chanels')

#SourcesData
class SourceForm(forms.ModelForm):
    class Meta:
        model = SourcesData
        fields = '__all__'
        #labels = {}
        #token = self.request.session["token"]
        widgets = {
            'sourcename': forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Введи имя'}),
            'token': forms.TextInput(attrs = {'class':'form-control'}),
            }
             
class SourcesDataCreate(CreateView):
    form_class = SourceForm
    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(SourcesDataCreate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        if "token" in self.request.session:
            initial['token'] = self.request.session['token']
            del self.request.session['token']

        # etc...
        return initial

    '''def get_context_data(self, **kwargs):
        """Use this to add extra context."""
        context = super(SourcesDataCreate, self).get_context_data(**kwargs)
        context['message'] = "111111"
        return context'''


    model = SourcesData
    success_url = reverse_lazy('sources')

class SourcesDataUpdate(UpdateView):
    form_class = SourceForm
    model = SourcesData
    success_url = reverse_lazy('sources')
    #fields = ['first_name','last_name','date_of_birth','date_of_death']

class SourcesDataDelete(DeleteView):
    model = SourcesData
    success_url = reverse_lazy('sources')


#Period


class PeriodForm(forms.ModelForm):
    def clean_days(self):
        data = self.cleaned_data['days']
        #Проверка того, что количество дней не отрицательно
        if data < 0:
            raise ValidationError('День не может быть отрицательным')
       # Не забывайте всегда возвращать очищенные данные
        return data
    def clean_hour(self):
        data = self.cleaned_data['hour']
           #Проверка того, что количество часов не отрицательно
        if data < 0:
            raise ValidationError('Часы не могут быть отрицательным')
           #Не забывайте всегда возвращать очищенные данные
        return data
    def clean_minutes(self):
        data = self.cleaned_data['minutes']
        if data < 0:
            raise ValidationError('Минуты не могут быть отрицательным')
       # Не забывайте всегда возвращать очищенные данные
        return data

    class Meta:
        model = Period
        fields = '__all__'
        

class PeriodCreate(CreateView):
    form_class = PeriodForm
    model = Period
    success_url = reverse_lazy('periods')

class PeriodUpdate(UpdateView):
    form_class = PeriodForm
    model = Period
    success_url = reverse_lazy('periods')
   

class PeriodDelete(DeleteView):
    model = Period
    success_url = reverse_lazy('periods')

#--------------------------------------
class SheduleCreate(CreateView):
    model = Shedule
    fields = '__all__'
    initial={'minute':'*','hour':'*', 'day':'*','month':'*','dayofmount':'*'}
    success_url = reverse_lazy('shedules')

class SheduleUpdate(UpdateView):
    model = Shedule
    fields = '__all__'
    success_url = reverse_lazy('shedules')
   

class SheduleDelete(DeleteView):
    model = Shedule
    success_url = reverse_lazy('shedules')
#----------------------------------------

class UrlsCreate(CreateView):
    model = Urls
    fields = '__all__'
    success_url = reverse_lazy('urls')

class UrlsUpdate(UpdateView):
    model = Urls
    fields = '__all__'
    success_url = reverse_lazy('urls')
   
class UrlsDelete(DeleteView):
    model = Urls
    success_url = reverse_lazy('urls')