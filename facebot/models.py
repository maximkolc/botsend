from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from datetime import datetime
from datetime import timedelta
from datetime import time
from facebot.tasks import send_mess
from django.db.models import signals
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    """
    Модель которая описыват задачу, для выполнения боту!!!
    """
    FILE_TYPES = (
        ('GIF', 'Гифки'),
        ('TXT', 'Тескс Markdown'),
        ('PNG', 'Картинки'),
    )
    REACTION = (
        ('yes','Да'),
        ('no', 'Нет')
        )
    
    taskname = models.CharField('Имя задачи',max_length=25, unique = True)
    chanelforpublic = models.ForeignKey('Chanels',  on_delete=models.SET_NULL, null=True, help_text ='Канал для публикации')
    momentforwork = models.TimeField('Время',max_length=25,help_text = 'Время следущей публикации, ЧЧ:ММ:СС')
    peripd_pub = models.ForeignKey('Period', null = True, help_text = 'Период публикации')
    sourcefordownload = models.ForeignKey('SourcesData', help_text="Источник данных для задачи" ,on_delete=models.SET_NULL, null=True)
    filetypesforload = models.CharField('Тип ресурсов',max_length=3,choices=FILE_TYPES, default= 'GIF')
    catalog = models.ForeignKey('Folders', on_delete=models.SET_NULL, null=True, help_text ='Каталог на диске')
    reactioan = models.CharField('Наличие реакций',max_length=3,choices=REACTION,default='yes')
    numfileforpub = models.IntegerField('Количесто публикуемых файлов')
    caption = models.CharField('Подпись',max_length=120)
    url = models.ManyToManyField('Urls', help_text="Исрользовать ссылки",null=True)
    bottoken = models.ForeignKey('MyBot', help_text = 'Бот для выполнения задачи',on_delete=models.SET_NULL, null=True)
    time_run = models.DateTimeField('Время запуска',blank=True,max_length=25,null=True,help_text = 'Дата и время очередного запуска')
    time_period = models.DurationField(null=True)
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    class Meta:
        ordering = ["momentforwork"]
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.taskname
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('task-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        #if self.time_run.seconds<timezone.now().seconds:
        #    self.time_run = null
        self.time_period = timedelta(days=self.peripd_pub.days, 
                                     hours=self.peripd_pub.hour, 
                                     minutes = self.peripd_pub.minutes)
        if self.time_run == None or self.time_run < timezone.now():
            #self.time_run = self.time_period.+self.momentforwork
            self.time_run = datetime.combine(datetime.now(), self.momentforwork) +self.time_period
        
        super(Task, self).save(*args, **kwargs) # Call the "real" save() method.'''
        
    
def task_save(sender, instance, signal, *args, **kwargs):
    #if not instance.is_verified:
    #Send verification email
    send_mess.delay(instance.id)

signals.post_save.connect(task_save, sender=Task)

class Chanels(models.Model):
    chanelname = models.CharField(max_length=25, unique = True, help_text = 'Имя канала')
    description = models.CharField(max_length=120, help_text = 'Описание')
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.chanelname
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return #reverse('chanel-detail', args=[str(self.id)])

class SourcesData(models.Model):
    sourcename = models.CharField('Имя',max_length=25, unique = True, help_text = 'Произвольное имя источника')
    password = models.CharField('Пароль', max_length=120, help_text = 'Пароль от яндекс диска')
    login  = models.CharField('Логин',max_length=120, help_text = 'Логин от яндекс диска')
    urls = models.CharField('Сервер',max_length=120, help_text = 'Адрес WebDav сервера')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.sourcename
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return #reverse('sourcename-detail', args=[str(self.id)])

class Urls(models.Model):
    urlname = models.CharField(max_length=120, unique = True, help_text = 'Имя ссылки')
    url = models.URLField(max_length=120, help_text = 'url адресс ссылки')
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.urlname
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return #reverse('urlname-detail', args=[str(self.id)])

class MyBot(models.Model):
    botname = models.CharField(max_length=120, unique = True, help_text = 'Имя бота')
    bottoken = models.CharField(max_length=120, unique = True, help_text = 'Токен бота')
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.botname
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return #reverse('botname-detail', args=[str(self.id)])

class Folders(models.Model):
    name = models.CharField('Имя',max_length=120, unique = True, help_text = 'Имя папки')
    description = models.CharField('Описание',max_length=120)
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return

class Period(models.Model):
    name = models.CharField('Имя',max_length=120, unique = True,null = True,  help_text = 'Уникальное имя')
    days = models.IntegerField('Дни', null = True, help_text = 'Количество дней')
    hour = models.IntegerField('Часы', null = True, help_text = 'Количество часов')
    minutes = models.IntegerField('Минуты', null = True, help_text = 'Количество минут')
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return