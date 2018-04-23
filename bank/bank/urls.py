"""bank URL Configuration

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
from django.conf.urls import url, include
from order import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^api/csSetUser/',views.csSetUser),
    # url(r'^api/csGetUser/', views.csGetUser),
    # url(r'^api/csRemoveUser/', views.csRemoveUser),
    # url(r'^api/csForm/', views.csForm),

    url(r'^api/getUser', views.getUser),
    url(r'^api/setUser', views.setUser),
    url(r'^api/removeUser', views.removeUser),
    url(r'^api/form', views.form),

    url(r'^home', views.home),
    url(r'^$', views.home),

    url(r'^submit', views.submit),
    url(r'^data', views.data),
    url(r'^edit/editUser', views.editUser),
    url(r'^edit/addu', views.editu),

    url(r'^edit', views.edit),
    url(r'^welcome', views.welcome),
    url(r'^search/tab', views.tab),

    url(r'^search', views.search),

    url(r'^login/', views.api_login),
    url(r'^index/', views.api_login),
    url(r'^api/login', views.api_login),
    url(r'^api/check', views.api_check),
    url(r'^api/logout', views.logout),
    url(r'^api/getAll', views.api_getall),
    url(r'^cs', views.cs),

]
