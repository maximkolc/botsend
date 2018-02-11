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
    user = models.OneToOneField(User, on_delete=models.CASCADE,  null=True)
    telegramm = models.CharField(blank=True, max_length=20)    
    activation_key = models.CharField(max_length=255, default=1)
    email_validated = models.BooleanField(default=False)

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
        #if self.time_run.seconds<timezone.now().seconds:
        #    self.time_run = null
        #self.time_period = timedelta(days=self.peripd_pub.days, 
        #                             hours=self.peripd_pub.hour, 
        #                             minutes = self.peripd_pub.minutes)
        #if self.time_run == None or self.time_run < timezone.now():
            #self.time_run = self.time_period.+self.momentforwork
        #    self.time_run = datetime.combine(datetime.now(), self.momentforwork) +self.time_period
        if self.caption == '':
            self.caption = "Нет"
        
        super(Task, self).save(*args, **kwargs) # Call the "real" save() method.'''
        
    
def task_save(sender, instance, signal, *args, **kwargs):
    #if not instance.is_verified:
    #Send verification email
    send_mess.delay(instance.id)

class OnceTask(models.Model):
    name = models.CharField("Имя задачи", max_length=25, unique = True)
    imgs = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/no-img.png')
    text =  models.CharField('Описание',max_length=600, help_text = 'Описание')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    run_date = models.DateTimeField("Время запуска", null=True)
    

class Chanels(models.Model):
    chanelname = models.CharField('Имя канала',max_length=25, unique = True, help_text = 'Имя канала')
    description = models.CharField('Описание',max_length=120, help_text = 'Описание')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.chanelname+" ("+self.description+")"
    
    
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
        return self.desc+" ("+self.ftype+")"
    
    
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

'''class Telega(models.Model):
    phone_number = models.CharField('Tel',max_length=12, unique = True,null = True,  help_text = 'Tel')
    code = models.CharField('code',max_length=12, unique = True,null = True,  help_text = 'code')'''
    

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