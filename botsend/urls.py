"""botsend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import django
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^admin/jsi18n', django.views.i18n.javascript_catalog),
    #url(r'/^media/admin/css/', django.contrib.admin),
    url(r'^admin/', admin.site.urls),

]
# Используйте include() чтобы добавлять URL из каталога приложения 
from django.conf.urls import include
urlpatterns += [
    url(r'^facebot/', include('facebot.urls')),
]
urlpatterns += [
    url(r'^telegabot/', include('facebot.urls')),
]
# Добавьте URL соотношения, чтобы перенаправить запросы с корневового URL, на URL приложения 
from django.views.generic import RedirectView
urlpatterns += [
    url(r'^$', RedirectView.as_view(url='/facebot/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf.urls import url, include
from markdownx import urls as markdownx

urlpatterns += [
    url(r'^markdownx/', include(markdownx))
]