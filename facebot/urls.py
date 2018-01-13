from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tasks/$', views.TaskListView.as_view(), name='tasks'),
    url(r'^chanels/$', views.ChanelsListView.as_view(), name='chanels'),
    url(r'^bots/$', views.MyBotListView.as_view(), name='bots'),
    url(r'^sources/$', views.SourcesDataListView.as_view(), name='sources'),
    url(r'^shedules/$', views.SheduleListView.as_view(), name='shedules'),
    url(r'^urls/$', views.UrlsListView.as_view(), name='urlss'),
    url(r'^run/(?P<id_task>\d+)/$', views.test_run, name='test_run'),
    url(r'^logs/$', views.logs),
    url(r'^log_detail/(?P<log_file>.+)/$', views.log_detail, name='log_detail'),
    url(r'^tokens/$', views.gettoken, name='tokens'),
    url(r'^ajax/getfolder/(?P<pk>\d+)/$', views.getfolder, name='getfolder'),
]

urlpatterns += [  
    url(r'^tasks/create/$', views.TaskCreate.as_view(), name='task_create'),
    url(r'^tasks/(?P<pk>\d+)/update/$', views.TaskUpdate.as_view(), name='task_update'),
    url(r'^tasks/(?P<pk>\d+)/delete/$', views.TaskDelete.as_view(), name='task_delete'),
    
]
urlpatterns += [  
    url(r'^bots/create/$', views.MyBotCreate.as_view(), name='mybot_create'),
    url(r'^bots/(?P<pk>\d+)/update/$', views.MyBotUpdate.as_view(), name='mybot_update'),
    url(r'^bots/(?P<pk>\d+)/delete/$', views.MyBotDelete.as_view(), name='mybot_delete'),
]
urlpatterns += [  
    url(r'^chanels/create/$', views.ChanelsCreate.as_view(), name='chanels_create'),
    url(r'^chanels/(?P<pk>\d+)/update/$', views.ChanelsUpdate.as_view(), name='chanels_update'),
    url(r'^chanels/(?P<pk>\d+)/delete/$', views.ChanelsDelete.as_view(), name='chanels_delete'),
]
urlpatterns += [  
    url(r'^chanels/create/$', views.ChanelsCreate.as_view(), name='chanels_create'),
    url(r'^chanels/(?P<pk>\d+)/update/$', views.ChanelsUpdate.as_view(), name='chanels_update'),
    url(r'^chanels/(?P<pk>\d+)/delete/$', views.ChanelsDelete.as_view(), name='chanels_delete'),
]
urlpatterns += [  
    url(r'^sources/create/$', views.SourcesDataCreate.as_view(), name='sources_create'),
    #url(r'^sources/add/$', views.add_token, name='add_token'),
    url(r'^sources/(?P<pk>\d+)/update/$', views.SourcesDataUpdate.as_view(), name='sources_update'),
    url(r'^sources/(?P<pk>\d+)/delete/$', views.SourcesDataDelete.as_view(), name='sources_delete'),
]

urlpatterns += [  
    url(r'^shedule/create/$', views.SheduleCreate.as_view(), name='shedule_create'),
    url(r'^shedule/(?P<pk>\d+)/update/$', views.SheduleUpdate.as_view(), name='shedule_update'),
    url(r'^shedule/(?P<pk>\d+)/delete/$', views.SheduleDelete.as_view(), name='shedule_delete'),
]
urlpatterns += [  
    url(r'^urls/create/$', views.UrlsCreate.as_view(), name='urls_create'),
    url(r'^urls/(?P<pk>\d+)/update/$', views.UrlsUpdate.as_view(), name='urls_update'),
    url(r'^urls/(?P<pk>\d+)/delete/$', views.UrlsDelete.as_view(), name='urls_delete'),
]
urlpatterns +=[
    url(r'^register/$', views.RegisterFormView.as_view(),name='register'),
    url(r'^login/$', views.LoginFormView.as_view(), name = 'login' ),
    url(r'^logout/$', views.LogoutView.as_view(), name = 'logout'),
]
