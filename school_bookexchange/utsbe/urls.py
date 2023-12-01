"""utsbe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from utsbookex import views
from django.conf.urls import include, url
from . import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    url(r'^utsbookex/', include('utsbookex.urls')),
    url(r'^$', views.index, name="index"),
    path('uts-be-detail-shop', views.utsbe, name = 'utsbe'),
    path('uts-be-shop', views.utsbe_shop, name = 'utsbe_shop'),
    path('uts-be-userprofile-display', views.utsbe_prf_books, name = 'utsbe_prf_books'),
    path('uts-be-book-edit', views.utsbe_bookedit, name = 'utsbe_bookedit'),
    path('uts-be-userprofile', views.utsbe_profileedit, name = 'utsbe_profileedit'),
    path('uts-be-udel', views.deletee, name = 'deletee')

]
"""   path('importfile', views.importfile, name = 'importfile') 
"""
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)