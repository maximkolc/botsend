from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
import datetime
from django import forms
from .forms import EditTaskForm
from django.contrib.admin import widgets 
import requests

#from .forms import RenewTaskForm

# Create your views here.
from .models import Task, Chanels, SourcesData, Urls, MyBot, Folders, Period,Shedule
from django.views import generic

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
def gettoken():
    url = 'https://oauth.yandex.ru/authorize'
    base_headers = {"response_type": "token","client_id": "55cd708ef7764279ace87970649d86d1"}
  

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

class FoldersListView(generic.ListView):
    model = Folders

class PeriodListView(generic.ListView):
    model = Period

class SheduleListView(generic.ListView):
    model = Shedule

class UrlsListView(generic.ListView):
    model = Urls


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        #exclude = ['time_run','time_period','momentforwork','peripd_pub']
        fields = '__all__'
        widgets = {
            #'momentforwork': widgets.AdminTimeWidget()
            'url': forms.CheckboxSelectMultiple(attrs={'style' : 'list-style-type: none'}),
            'filetypesforload': forms.CheckboxSelectMultiple(attrs={'style' : 'list-style-type: none'})


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
class SourcesDataCreate(CreateView):
    model = SourcesData
    fields = '__all__'
    initial={'urls':'https://webdav.yandex.ru',}
    success_url = reverse_lazy('sources')

class SourcesDataUpdate(UpdateView):
    model = SourcesData
    fields = '__all__'
    success_url = reverse_lazy('sources')
    #fields = ['first_name','last_name','date_of_birth','date_of_death']

class SourcesDataDelete(DeleteView):
    model = SourcesData
    success_url = reverse_lazy('sources')

#Folders
class FoldersCreate(CreateView):
    model = Folders
    fields = '__all__'
    success_url = reverse_lazy('folders')

class FoldersUpdate(UpdateView):
    model = Folders
    fields = '__all__'
    success_url = reverse_lazy('folders')

class FoldersDelete(DeleteView):
    model = Folders
    success_url = reverse_lazy('folders')

#Period
'''class CustomAdminSplitDateTime(AdminSplitDateTime):
    def __init__(self, attrs=None):
        widgets = [widgets.AdminDateWidget, widgets.AdminTimeWidget(attrs=None, format='%I:%M %p')]
        forms.MultiWidget.__init__(self, widgets, attrs)'''

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