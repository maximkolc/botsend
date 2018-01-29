from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.db.models import signals
from django.utils import timezone
from crontab import CronTab
#------------для работы с пользователями------------------------
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#---------------------------------------------------------------
import logging
import getpass
#---------модель для профиля пользователя-----------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
#----------------------------------------------------------------

# Create your models here.

class Task(models.Model):
    """
    Модель которая описыват задачу, для выполнения боту!!!
    """
    '''FILE_TYPES = (
        ('GIF', 'Гифки'),
        ('TXT', 'Тескс Markdown'),
        ('PNG', 'Картинки'),
    )'''
    REACTION = (
        ('yes','Да'),
        ('no', 'Нет')
        )
    
    taskname = models.CharField('Имя задачи',max_length=25, unique = True)
    chanelforpublic = models.ForeignKey('Chanels',  on_delete=models.SET_NULL, null=True, help_text ='Канал для публикации')
    sourcefordownload = models.ForeignKey('SourcesData', help_text="Источник данных для задачи" ,on_delete=models.SET_NULL, null=True)
    filetypesforload = models.ManyToManyField('FileTypeChoices',null=True)
    #catalog = models.ForeignKey('Folders', on_delete=models.SET_NULL, null=True, help_text ='Каталог на диске')
    catalog_ajax = models.CharField('Каталог на диске', max_length = 30, blank= True, null = True)
    #reactioan = models.CharField('Наличие реакций',max_length=3,choices=REACTION,default='yes')
    numfileforpub = models.IntegerField('Количесто публикуемых файлов')
    caption = models.CharField('Подпись',max_length=120, blank=True)
    url = models.ManyToManyField('Urls', help_text="Исрользовать ссылки",null=True, blank=True)
    bottoken = models.ForeignKey('MyBot', help_text = 'Бот для выполнения задачи',on_delete=models.SET_NULL, null=True)
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    class Meta:
        ordering = ["chanelforpublic"]
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
        #self.time_period = timedelta(days=self.peripd_pub.days, 
        #                             hours=self.peripd_pub.hour, 
        #                             minutes = self.peripd_pub.minutes)
        #if self.time_run == None or self.time_run < timezone.now():
            #self.time_run = self.time_period.+self.momentforwork
        #    self.time_run = datetime.combine(datetime.now(), self.momentforwork) +self.time_period
        
        super(Task, self).save(*args, **kwargs) # Call the "real" save() method.'''
        
    
def task_save(sender, instance, signal, *args, **kwargs):
    #if not instance.is_verified:
    #Send verification email
    send_mess.delay(instance.id)


class Chanels(models.Model):
    chanelname = models.CharField('Имя канала',max_length=25, unique = True, help_text = 'Имя канала')
    description = models.CharField('Описание',max_length=120, help_text = 'Описание')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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
    sourcename = models.CharField('Имя',max_length=25, unique = True, help_text = 'Произвольное имя источника', null = True)
    token = models.CharField('Токен',max_length=50, help_text = 'отладочный токен ядиска', null = True) 
    #password = models.CharField('Пароль', max_length=120, help_text = 'Пароль от яндекс диска')
    #login  = models.CharField('Логин',max_length=120, help_text = 'Логин от яндекс диска')
    #urls = models.CharField('Сервер',max_length=120, help_text = 'Адрес WebDav сервера')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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

class FileTypeChoices(models.Model):
    desc = models.CharField(max_length=120,  help_text = 'Описание', null=True)
    ftype = models.CharField(max_length=120, help_text = 'расширение без точки', unique = True, null=True)
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.desc
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return #reverse('desc-detail', args=[str(self.id)])


class MyBot(models.Model):
    botname = models.CharField('Имя бота',max_length=120, unique = True, help_text = 'Имя бота')
    bottoken = models.CharField('Токен бота',max_length=120, unique = True, help_text = 'Токен бота')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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



class Shedule(models.Model):
    name = models.CharField('Имя',max_length=120, unique = True,null = True,  help_text = 'Уникальное имя')
    minute = models.CharField('Минута', null = True, help_text = 'минута',max_length=12)
    hour = models.CharField('Час', null = True, help_text = 'Час',max_length=12)
    day = models.CharField('День', null = True, help_text = 'День',max_length=12)
    month = models.CharField('Месяц', null = True, help_text = 'Месяц',max_length=12)
    dayofmount = models.CharField('День недели', null = True, help_text = 'День недели',max_length=12)
    task = models.ManyToManyField(Task, help_text = 'Задача для выполнения', null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return

    

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
    com1 = '/home/maxim/work/botenv2/bin/python  /home/maxim/work/botsend/manage.py crontask '
    com2 = 'python3  ~/botsend/manage.py crontask '
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