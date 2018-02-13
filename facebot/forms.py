from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Task, Chanels, SourcesData, Urls, MyBot,Shedule, OnceTask
from django.views import generic
from django.contrib.auth import logout
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm   
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from datetimewidget.widgets import DateTimeWidget
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class LoginFormView(FormView):
    form_class = AuthenticationForm
    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "login.html"
    # В случае успеха перенаправим на главную.
    success_url = reverse_lazy("index")
    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()
        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Имя рользователя', min_length=4, max_length=150)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Пользователь с таким именем уже существует")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email уже занят")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


'''class RegisterFormView(FormView):
    form_class = UserCreationForm
    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = reverse_lazy("login")
    email = forms.EmailField(required=True)
    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()
        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)'''

class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect(reverse('login'))


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



#MyBot
#-----------------------------------------------------------
class MyBotForm(forms.ModelForm):
    class Meta:
        model = MyBot
        #fields = '__all__'
        exclude = ['created_by']

class MyBotCreate(LoginRequiredMixin,CreateView):
    form_class = MyBotForm
    model = MyBot
    success_url = reverse_lazy('bots')
    login_url = reverse_lazy("login")
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save() 
        return HttpResponseRedirect(reverse('bots'))

class MyBotUpdate(LoginRequiredMixin,UpdateView):
    form_class = MyBotForm
    model = MyBot
    success_url = reverse_lazy('bots')
    login_url = reverse_lazy("login")
   

class MyBotDelete(LoginRequiredMixin,DeleteView):
    model = MyBot
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('bots')

class TaskListView(LoginRequiredMixin,generic.ListView):
    #model = Task
    login_url = reverse_lazy("login")
    def get_queryset(self):
        """Returns Chanels that belong to the current user"""
        return Task.objects.filter(created_by=self.request.user)
    
class TaskDetailView(LoginRequiredMixin,generic.DetailView):
    model = Task

class ChanelsListView(LoginRequiredMixin,generic.ListView):
    #model = Chanels
    login_url = reverse_lazy("login")
    def get_queryset(self):
        """Returns Chanels that belong to the current user"""
        return Chanels.objects.filter(created_by=self.request.user)
   

class MyBotListView(LoginRequiredMixin,generic.ListView):
    #model = MyBot
    login_url = reverse_lazy("login")
    def get_queryset(self):
        """Returns Chanels that belong to the current user"""
        return MyBot.objects.filter(created_by=self.request.user) 

class SourcesDataListView(LoginRequiredMixin,generic.ListView):
    #model = SourcesData
    login_url = reverse_lazy("login")
    def get_queryset(self):
        """Returns Chanels that belong to the current user"""
        return SourcesData.objects.filter(created_by=self.request.user)




class SheduleListView(LoginRequiredMixin,generic.ListView):
    #model = Shedule
    login_url = reverse_lazy("login")
    def get_queryset(self):
        """Returns Chanels that belong to the current user"""
        return Shedule.objects.filter(created_by=self.request.user)

class UrlsListView(LoginRequiredMixin,generic.ListView):
    #model = Urls
    login_url = reverse_lazy("login")
    def get_queryset(self):
        """Returns Chanels that belong to the current user"""
        return Urls.objects.filter(created_by=self.request.user)


class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Task
        #fields = '__all__'
        exclude = ['created_by']
        labels = {
            'chanelforpublic': 'Канал куда публикуем',
            'sourcefordownload': 'Яндекс диск',
            'filetypesforload': 'Типы публикуемых файлов',
            'bottoken': 'Публикующий бот',
            'url': 'Кнопки под публикацией',
            'catalog_ajax': 'Каталог на диске',

        }
        widgets = {
            'url': forms.CheckboxSelectMultiple(),
            'filetypesforload': forms.CheckboxSelectMultiple(),
            'taskname': forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Введи имя'}),
            'chanelforpublic': forms.Select(attrs={'class':'form-control'}),
            'sourcefordownload': forms.Select(attrs={'class':'form-control'}),
            'catalog_ajax': forms.Select(attrs={'class':'form-control'}),
            'numfileforpub': forms.NumberInput(attrs={'class':'form-control', 'min':1}),
            'num_file_min':forms.NumberInput(attrs={'class':'form-control', 'min':1,'placeholder':'от'}),
            'num_file_max':forms.NumberInput(attrs={'class':'form-control', 'min':1, 'placeholder':'до'}),
            'numfileforpub_random':forms.RadioSelect(),
            'caption':forms.Textarea(attrs = {'class':'form-control', 'placeholder':'','cols': 80, 'rows': 4}),
            'bottoken': forms.Select(attrs={'class':'form-control'}),
             }
             
class TaskCreate(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    model = Task
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('tasks')
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save() 
        return HttpResponseRedirect(reverse('tasks'))

class TaskUpdate(LoginRequiredMixin, UpdateView):
    form_class = TaskForm
    model = Task
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')

'''#MyBot
#-----------------------------------------------------------
class MyBotForm(forms.ModelForm):
    class Meta:
        model = MyBot
        #fields = '__all__'
        exclude = ['created_by']

class MyBotCreate(LoginRequiredMixin,CreateView):
    form_class = MyBotForm
    model = MyBot
    success_url = reverse_lazy('bots')
    login_url = reverse_lazy("login")
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save() 
        return HttpResponseRedirect(reverse('bots'))

class MyBotUpdate(LoginRequiredMixin,UpdateView):
    form_class = MyBotForm
    model = MyBot
    success_url = reverse_lazy('bots')
    login_url = reverse_lazy("login")
   

class MyBotDelete(LoginRequiredMixin,DeleteView):
    model = MyBot
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('bots')'''
#---------------------------------------------------------------
class MyChanelsForm(forms.ModelForm):
    class Meta:
        model = Chanels
        exclude = ['created_by']

class ChanelsCreate(LoginRequiredMixin,CreateView):
    form_class = MyChanelsForm
    model = Chanels
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('chanels')
    def form_valid(self, form):
        # Мы используем ModelForm, а его метод save() возвращает инстанс
        # модели, связанный с формой. Аргумент commit=False говорит о том, что
        # записывать модель в базу рановато.
        instance = form.save(commit=False)
        # Теперь, когда у нас есть несохранённая модель, можно ей чего-нибудь
        # накрутить. Например, заполнить внешний ключ на auth.User. У нас же
        # блог, а не анонимный имижборд, правда?
        instance.created_by = self.request.user
        # А теперь можно сохранить в базу
        instance.save() 
        
        return HttpResponseRedirect(reverse('chanels'))

class ChanelsUpdate(LoginRequiredMixin,UpdateView):
    form_class = MyChanelsForm
    model = Chanels
    login_url = reverse_lazy("login")
    success_url = reverse_lazy('chanels')
    

class ChanelsDelete(LoginRequiredMixin,DeleteView):
    model = Chanels
    success_url = reverse_lazy('chanels')

#SourcesData -------------------------------------------------

class SourceForm(forms.ModelForm):
    class Meta:
        model = SourcesData
        #fields = '__all__'
        exclude = ['created_by']
        widgets = {
            'sourcename': forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Введи имя'}),
            'token': forms.TextInput(attrs = {'class':'form-control'}),
            }
             
class SourcesDataCreate(LoginRequiredMixin,CreateView):
    form_class = SourceForm
    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(SourcesDataCreate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        if "token" in self.request.session:
            initial['token'] = self.request.session['token']
            del self.request.session['token']
        return initial
    model = SourcesData
    exclude = ['created_by']
    success_url = reverse_lazy('sources')
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save() 
        return HttpResponseRedirect(reverse('sources'))

class SourcesDataUpdate(LoginRequiredMixin,UpdateView):
    form_class = SourceForm
    model = SourcesData
    exclude = ['created_by']
    success_url = reverse_lazy('sources')
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save() 
        return HttpResponseRedirect(reverse('sources'))

class SourcesDataDelete(LoginRequiredMixin,DeleteView):
    model = SourcesData
    success_url = reverse_lazy('sources')



#--------------------------------------
class SheduleForm(forms.ModelForm):
    class Meta:
        model = Shedule
        #fields = '__all__'
        exclude = ['created_by']
        labels = {
            'task': 'Задания для выполнения',
        }
        widgets = {
            'task': forms.CheckboxSelectMultiple(attrs={'style' : 'list-style-type: none'})
        }
    # получаем только таски с действующем юзером
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SheduleForm, self).__init__(*args, **kwargs)
        self.fields['task'].queryset = Task.objects.filter(created_by = user)

class SheduleCreate(LoginRequiredMixin,CreateView):
    model = Shedule
    #fields = '__all__'
    form_class = SheduleForm
    # получаем только таски с действующем юзером продоложение
    def get_form_kwargs(self):
        kwargs = super(SheduleCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    initial={'minute':'*','hour':'*', 'day':'*','month':'*','dayofmount':'*'}
    success_url = reverse_lazy('shedules')
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        form.save_m2m() 
        return HttpResponseRedirect(reverse('shedules'))

class SheduleUpdate(LoginRequiredMixin,UpdateView):
    model = Shedule
    form_class = SheduleForm
    #fields = '__all__'
    success_url = reverse_lazy('shedules')
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        form.save_m2m()  
        return HttpResponseRedirect(reverse('shedules'))
   

class SheduleDelete(LoginRequiredMixin,DeleteView):
    model = Shedule
    success_url = reverse_lazy('shedules')
#----------------------------------------
class MyUrlsForm(forms.ModelForm):
    class Meta:
        model = Urls
        exclude = ['created_by']

class UrlsCreate(LoginRequiredMixin,CreateView):
    form_class = MyUrlsForm
    model = Urls
    success_url = reverse_lazy('urlss')
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save() 
        return HttpResponseRedirect(reverse('urlss'))

class UrlsUpdate(LoginRequiredMixin,UpdateView):
    form_class = MyUrlsForm
    model = Urls
    success_url = reverse_lazy('urlss')
    '''def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save() 
        return HttpResponseRedirect(reverse('urlss'))'''
   
class UrlsDelete(LoginRequiredMixin,DeleteView):
    model = Urls
    success_url = reverse_lazy('urlss')



#-------------------------------------------
class UpdateForm(forms.ModelForm):
    #form for updating users
    #the field you want to use should already be defined in the model
    #so no need to add them here again DRY
    class Meta:
        model = User
        fields = ['username', 'email']

class UserUpdate(UpdateView):  
    context_object_name = 'variable_used_in `user_form.html`'
    form_class = UpdateForm
    template_name = 'facebot/user_form.html'
    success_url = reverse_lazy('profile')
    #get object
    def get_object(self, queryset=None): 
        return self.request.user
    #override form_valid method
    def form_valid(self, form):
        #save cleaned post data
        clean = form.cleaned_data 
        context = {}        
        self.object = context.save(clean) 
        return super(UserUpdate, self).form_valid(form) 
#-------------------------------------------
class OnceTaskUploadForm(forms.ModelForm):
    #text = forms.CharField( widget=forms.
    class Meta:
        model = OnceTask
        exclude = ['created_by']
        labels = {
            'chanelforpublic': 'Канал',
            'bottoken': 'Бот',
            'text' : 'Текст'
        }
        widgets = {
            'chanelforpublic': forms.Select(attrs={'class':'form-control'}),
            'bottoken': forms.Select(attrs={'class':'form-control'}),
            'run_date': DateTimeWidget(attrs={'class':"form-control"}, usel10n = True, bootstrap_version=3),
            'text': forms.Textarea(attrs={"data-provide":"markdown","name":"content","rows":"5",'cols':'1'}) 
             }       
    def __init__(self, *args, **kwargs):
        super(OnceTaskUploadForm, self).__init__(*args, **kwargs)
        self.fields['imgs'].widget.attrs.update({
            'name':'pic[]',
             'class' : 'photo' 
        })
class OnceTaskCreate(LoginRequiredMixin, CreateView):
    form_class = OnceTaskUploadForm
    model = OnceTask
    success_url = reverse_lazy('oncetasks')
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save()
        return HttpResponseRedirect(reverse('oncetasks'))

class OnceTaskUpdate(LoginRequiredMixin,UpdateView):
    form_class = OnceTaskUploadForm
    model = OnceTask
    success_url = reverse_lazy('oncetasks')
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.created_by = self.request.user
        instance.save() 
        return HttpResponseRedirect(reverse('oncetasks'))
   
class OnceTaskDelete(LoginRequiredMixin,DeleteView):
    model = OnceTask
    success_url = reverse_lazy('oncetasks')

class OnceTaskListView(LoginRequiredMixin,generic.ListView):
    #model = SourcesData
    login_url = reverse_lazy("login")
    def get_queryset(self):
        """Returns Chanels that belong to the current user"""
        return OnceTask.objects.filter(created_by=self.request.user)