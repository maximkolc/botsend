from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tasks/$', views.TaskListView.as_view(), name='tasks'),
    url(r'^chanels/$', views.ChanelsListView.as_view(), name='chanels'),
    url(r'^bots/$', views.MyBotListView.as_view(), name='bots'),
    url(r'^sources/$', views.SourcesDataListView.as_view(), name='sources'),
    url(r'^folders/$', views.FoldersListView.as_view(), name='folders'),
    url(r'^periods/$', views.PeriodListView.as_view(), name='periods'),
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
    url(r'^sources/(?P<pk>\d+)/update/$', views.SourcesDataUpdate.as_view(), name='sources_update'),
    url(r'^sources/(?P<pk>\d+)/delete/$', views.SourcesDataDelete.as_view(), name='sources_delete'),
]
urlpatterns += [  
    url(r'^folders/create/$', views.FoldersCreate.as_view(), name='folders_create'),
    url(r'^folders/(?P<pk>\d+)/update/$', views.FoldersUpdate.as_view(), name='folders_update'),
    url(r'^folders/(?P<pk>\d+)/delete/$', views.FoldersDelete.as_view(), name='folders_delete'),
]
urlpatterns += [  
    url(r'^periods/create/$', views.PeriodCreate.as_view(), name='periods_create'),
    url(r'^periods/(?P<pk>\d+)/update/$', views.PeriodUpdate.as_view(), name='periods_update'),
    url(r'^periods/(?P<pk>\d+)/delete/$', views.PeriodDelete.as_view(), name='periods_delete'),
]