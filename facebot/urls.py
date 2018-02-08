from django.conf.urls import url

from . import views
from . import forms
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tasks/$', forms.TaskListView.as_view(), name='tasks'),
    url(r'^chanels/$', forms.ChanelsListView.as_view(), name='chanels'),
    url(r'^bots/$', forms.MyBotListView.as_view(), name='bots'),
    url(r'^sources/$', forms.SourcesDataListView.as_view(), name='sources'),
    url(r'^shedules/$', forms.SheduleListView.as_view(), name='shedules'),
    url(r'^urls/$', forms.UrlsListView.as_view(), name='urlss'),
    url(r'^run/(?P<id_task>\d+)/$', views.test_run, name='test_run'),
    url(r'^logs/$', views.logs),
    url(r'^log_detail/(?P<log_file>.+)/$', views.log_detail, name='log_detail'),
    url(r'^tokens/$', views.gettoken, name='tokens'),
    url(r'^ajax/getfolder/(?P<pk>\d+)/$', views.getfolder, name='getfolder'),
]

urlpatterns += [  
    url(r'^tasks/create/$', forms.TaskCreate.as_view(), name='task_create'),
    url(r'^tasks/(?P<pk>\d+)/update/$', forms.TaskUpdate.as_view(), name='task_update'),
    url(r'^tasks/(?P<pk>\d+)/delete/$', forms.TaskDelete.as_view(), name='task_delete'),
    
]
urlpatterns += [  
    url(r'^bots/create/$', forms.MyBotCreate.as_view(), name='mybot_create'),
    url(r'^bots/(?P<pk>\d+)/update/$', forms.MyBotUpdate.as_view(), name='mybot_update'),
    url(r'^bots/(?P<pk>\d+)/delete/$', forms.MyBotDelete.as_view(), name='mybot_delete'),
]
urlpatterns += [  
    url(r'^chanels/create/$', forms.ChanelsCreate.as_view(), name='chanels_create'),
    url(r'^chanels/(?P<pk>\d+)/update/$', forms.ChanelsUpdate.as_view(), name='chanels_update'),
    url(r'^chanels/(?P<pk>\d+)/delete/$', forms.ChanelsDelete.as_view(), name='chanels_delete'),
]

urlpatterns += [  
    url(r'^sources/create/$', forms.SourcesDataCreate.as_view(), name='sources_create'),
    #url(r'^sources/add/$', views.add_token, name='add_token'),
    url(r'^sources/(?P<pk>\d+)/update/$', forms.SourcesDataUpdate.as_view(), name='sources_update'),
    url(r'^sources/(?P<pk>\d+)/delete/$', forms.SourcesDataDelete.as_view(), name='sources_delete'),
]

urlpatterns += [  
    url(r'^shedule/create/$', forms.SheduleCreate.as_view(), name='shedule_create'),
    url(r'^shedule/(?P<pk>\d+)/update/$', forms.SheduleUpdate.as_view(), name='shedule_update'),
    url(r'^shedule/(?P<pk>\d+)/delete/$', forms.SheduleDelete.as_view(), name='shedule_delete'),
]
urlpatterns += [  
    url(r'^urls/create/$', forms.UrlsCreate.as_view(), name='urls_create'),
    url(r'^urls/(?P<pk>\d+)/update/$', forms.UrlsUpdate.as_view(), name='urls_update'),
    url(r'^urls/(?P<pk>\d+)/delete/$', forms.UrlsDelete.as_view(), name='urls_delete'),
]
urlpatterns +=[
    url(r'^register/$', views.register,name='register'),
    url(r'^login/$', forms.LoginFormView.as_view(), name = 'login' ),
    url(r'^logout/$', forms.LogoutView.as_view(), name = 'logout'),
    url(r'^activate/account/$', views.activate_account, name='activate'),
    url(r'^password-change-done/$',
        auth_views.password_change_done,
        {'template_name': 'password_change_done.html'},
        name='password_change_done'),
    url(r'^password-change/$',
        auth_views.password_change,
       {'template_name': 'password_change.html' , 'post_change_redirect': 'password_change_done'},
        name='password_change'
    ),
]
