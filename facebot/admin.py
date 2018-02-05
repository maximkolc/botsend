from django.contrib import admin

# Register your models here.
from .models import Task, Chanels, SourcesData, Urls, MyBot,Shedule,FileTypeChoices, Profile

admin.site.register(Task)
admin.site.register(Chanels)
admin.site.register(SourcesData)
admin.site.register(Urls)
admin.site.register(MyBot)
admin.site.register(Shedule)
admin.site.register(FileTypeChoices)
admin.site.register(Profile)