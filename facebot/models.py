from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.db.models import signals
from facebot.tasks import send_once
from django.utils import timezone
from crontab import CronTab
#------------для работы с пользователями------------------------
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#---------------------------------------------------------------
import logging
import getpass
from datetime import datetime
from datetime import timedelta

#---------модель для профиля пользователя-----------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  null=True)
    telegramm = models.CharField(blank=True, max_length=20, default="не задано")    
    activation_key = models.CharField(max_length=255, default=1)
    email_validated = models.BooleanField(default=False)
    ip_adress = models.CharField(max_length=255, null = True)
    datetowork = models.DateTimeField(null=True)
    last_visit = models.DateTimeField(null = True)
    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('post_by_author', args=[self.user.username])

#@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

#@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
#----------------------------------------------------------------

# модель для сообщений пользователю от бота
class Messages(models.Model):
    '''
    Модель для сообщений пользователю от бота
    '''
    username = models.CharField('Имя пользователя', max_length = 30)
    text = models.CharField('Текст сообщения', max_length = 200)
    date = models.DateTimeField('Дата отправки')

# Create your models here.

class Task(models.Model):
    """
    Модель которая описыват задачу, для выполнения боту!!!
    """
    REACTION = (
        ('yes','Да'),
        ('no', 'Нет')
        )
    BOOL_CHOICES = ((True, ' Случайно'), (False, 'Вручную'))
    IS_DEL = ((True, 'Да'), (False, 'Нет'))
    taskname = models.CharField('Имя задачи',max_length=25)
    chanelforpublic = models.ForeignKey('Chanels',  on_delete=models.SET_NULL, null=True, help_text ='Канал для публикации')
    sourcefordownload = models.ForeignKey('SourcesData', help_text="Источник данных для задачи" ,on_delete=models.SET_NULL, null=True)
    filetypesforload = models.ManyToManyField('FileTypeChoices',null=True)
    catalog_ajax = models.CharField('Каталог на диске', max_length = 30, blank= True, null = True)
    # поля для обработки количества публикуемых файлов
    numfileforpub = models.IntegerField('Количесто публикуемых файлов')
    numfileforpub_random =  models.BooleanField('Случайно',default = False, choices=BOOL_CHOICES)
    num_file_min = models.IntegerField('Минимальное количесто публикуемых файлов', null = True, blank=True)
    num_file_max = models.IntegerField('Максимальное количесто публикуемых файлов', null = True, blank=True)
    # -----
    caption = models.CharField('Подпись',max_length=120, blank=True)
    url = models.ManyToManyField('Urls', help_text="Исрользовать ссылки",null=True, blank=True)
    bottoken = models.ForeignKey('MyBot', help_text = 'Бот для выполнения задачи',on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    isfiledelete = models.BooleanField('Нет',default = False, choices=IS_DEL)
    status = models.CharField('Статус',max_length=25, null = True)
    class Meta:
        ordering = ["chanelforpublic"]
        unique_together = ('taskname', 'created_by')
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
        if self.caption == '':
            self.caption = "Нет"
        super(Task, self).save(*args, **kwargs) # Call the "real" save() method.'''
        
    
'''def task_save(sender, instance, signal, *args, **kwargs):
    #if not instance.is_verified:
    #Send verification email
    send_mess.delay(instance.id)'''

# Models
class ImageUpload(models.Model):
        model_pic = models.ImageField(upload_to='pic_folder/', null=True)

class OnceTask(models.Model):
    MESSAGE_TYPE = (('text', ' Текст'), ('photo', 'Картинка с подписью'))
    name = models.CharField("Имя задачи", max_length=25)
    #imgs = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/no-img.png')
    text =  models.CharField('Описание',max_length=6000, help_text = 'Описание')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    run_date = models.DateTimeField("Время запуска", null=True)
    del_date = models.DateTimeField("Время удаления", null=True)
    chanelforpublic = models.ManyToManyField('Chanels',  null=True, help_text ='Канал для публикации')
    bottoken = models.ForeignKey('MyBot', help_text = 'Бот для выполнения задачи',on_delete=models.SET_NULL, null=True)
    status = models.CharField("Статус", max_length=25, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    type_mes =  models.CharField('Тип контента',max_length=10,default = 'text', choices= MESSAGE_TYPE )
    
    #class Meta:
        #unique_together = ('name', 'created_by')

    '''def save(self, *args, **kwargs):
        self.status = "Ожидает выполнения "+ str(self.run_date)
        super(OnceTask, self).save(*args, **kwargs) # Call the real save() method'''

def oncetask_post_save(sender, instance, signal, *args, **kwargs):
    #send_once.delay(instance.id)
    #print ("SECONDS:" + str(instance.run_date))
    #print ("SECONDS:" + str(datetime.now()))
    #print((instance.run_date.replace(tzinfo=None) - datetime.now()).total_seconds())
    #instance.status = "Ожидает выполнения "+ str(instance.run_date)
    OnceTask.objects.filter(id=instance.id).update(status = "Ожидает выполнения "+ str(instance.run_date))
    send_once.apply_async([instance.id], countdown=(instance.run_date.replace(tzinfo=None) - datetime.now()).total_seconds())
    #print ("SECONDS:" + str((instance.run_date - datetime.now()).total_seconds()))
signals.post_save.connect(oncetask_post_save, sender=OnceTask)


class Chanels(models.Model):
    chanelname = models.CharField('Имя канала',max_length=25,  help_text = 'Имя канала')
    description = models.CharField('Описание',max_length=120, help_text = 'Описание')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.chanelname+" ("+self.description+")"
    class Meta:
        unique_together = ('chanelname', 'created_by')
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return #reverse('chanel-detail', args=[str(self.id)])

class SourcesData(models.Model):
    sourcename = models.CharField('Имя',max_length=25, help_text = 'Произвольное имя источника', null = True)
    token = models.CharField('Токен',max_length=50, help_text = 'отладочный токен ядиска', null = True) 
    #password = models.CharField('Пароль', max_length=120, help_text = 'Пароль от яндекс диска')
    #login  = models.CharField('Логин',max_length=120, help_text = 'Логин от яндекс диска')
    #urls = models.CharField('Сервер',max_length=120, help_text = 'Адрес WebDav сервера')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    class Meta:
        unique_together = ('sourcename', 'created_by')
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
    urlname = models.CharField(max_length=120, help_text = 'Имя ссылки')
    url = models.URLField(max_length=120, help_text = 'url адресс ссылки')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.urlname
    class Meta:
        unique_together = ('urlname', 'created_by')
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return #reverse('urlname-detail', args=[str(self.id)])

class FileTypeChoices(models.Model):
    desc = models.CharField(max_length=120,  help_text = 'Описание', null=True)
    ftype = models.CharField(max_length=120, help_text = 'расширение без точки', unique = True, null=True)
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.desc+" ("+self.ftype+")"
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return #reverse('desc-detail', args=[str(self.id)])


class MyBot(models.Model):
    botname = models.CharField('Имя бота',max_length=120, help_text = 'Имя бота')
    bottoken = models.CharField('Токен бота',max_length=120, help_text = 'Токен бота')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.botname
    class Meta:
        unique_together = ('botname', 'created_by','bottoken')
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return #reverse('botname-detail', args=[str(self.id)])



class Shedule(models.Model):
    name = models.CharField('Имя',max_length=120, null = True,  help_text = 'Уникальное имя')
    minute = models.CharField('Минута', null = True, help_text = 'минута',max_length=12)
    hour = models.CharField('Час', null = True, help_text = 'Час',max_length=12)
    day = models.CharField('День', null = True, help_text = 'День',max_length=12)
    month = models.CharField('Месяц', null = True, help_text = 'Месяц',max_length=12)
    dayofmount = models.CharField('День недели', null = True, help_text = 'День недели',max_length=12)
    task = models.ManyToManyField(Task, help_text = 'Задача для выполнения', null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    class Meta:
        unique_together = ('name', 'created_by')
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return

'''class Telega(models.Model):
    phone_number = models.CharField('Tel',max_length=12, unique = True,null = True,  help_text = 'Tel')
    code = models.CharField('code',max_length=12, unique = True,null = True,  help_text = 'code')'''


class MessageReaction(models.Model):
    '''
    Модель для сохранения результатов лайков, дизлайков
    '''
    chat_id = models.CharField("ид чата", max_length = 120, null = True)
    message_id = models.CharField("ид собщения", max_length = 120, null = True)
    like_count = models.IntegerField("количество лайков", null = True)
    dislike_count = models.IntegerField("количество лайков", null = True)
    username = models.CharField("Имя пользователя", max_length = 120, null = True)
    chanel_name = models.CharField("Имя канала", max_length = 120, null = True)

def task_add_cron(sender, instance, signal, *args, **kwargs):
    #logging.basicConfig(filename="sample.log",format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    logger = logging.getLogger("model")
    logger.setLevel(logging.INFO)
    # create the logging file handler
    fh = logging.FileHandler("logs/models.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)
    com2 = '/home/maxim/work/botenv2/bin/python  /home/maxim/work/botsend/manage.py crontask '
    com1 = 'python3  ~/botsend/manage.py crontask '
    #user = getpass.getuser()
    t_id=[]
    for task in instance.task.all():
        t_id.append(str(task.id))
    print ("lengt: "+str(len(t_id)))
    print(' '.join(t_id))
    my_cron = CronTab(user=getpass.getuser())
    flag = True
    for job in my_cron:
        if job.comment == str(instance.id):
            logger.info("Изменение существующей задачи "+ str(instance.id))
            my_cron.remove(job)
            #job = my_cron.new(command=com2+str(instance.task.id), comment=str(instance.id))
            job = my_cron.new(command=com2+' '.join(t_id), comment=str(instance.id))
            job.setall(instance.minute, instance.hour, instance.day, instance.month, instance.dayofmount)
            my_cron.write()
            flag = False
            logger.info("запись успешно изменена")
    if flag:
        job = my_cron.new(command=com2+' '.join(t_id), comment=str(instance.id))
        job.setall(instance.minute, instance.hour, instance.day, instance.month, instance.dayofmount)
        my_cron.write()

def task_del_cron(sender, instance, signal, *args, **kwargs):
    #logging.basicConfig(filename="sample.log",format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    logger = logging.getLogger("model")
    logger.setLevel(logging.INFO)
    # create the logging file handler
    fh = logging.FileHandler("logs/models.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)
    my_cron = CronTab(user=getpass.getuser()) #'gash_ne')
    for job in my_cron:
        logger.info("Зашли в удаление")
        logger.info(instance.id)
        if job.comment == str(instance.id):
            logger.info("Нашли и удаляем")
            my_cron.remove(job)
            my_cron.write()
    
signals.m2m_changed.connect(task_add_cron, sender=Shedule.task.through)
signals.post_delete.connect(task_del_cron, sender=Shedule)