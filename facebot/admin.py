from django.contrib import admin

# Register your models here.
from .models import Task, Chanels, SourcesData, Urls, MyBot

admin.site.register(Task)
admin.site.register(Chanels)
admin.site.register(SourcesData)
admin.site.register(Urls)
admin.site.register(MyBot)