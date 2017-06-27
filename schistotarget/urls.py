"""schistotarget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from app import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='index'),
    url(r'^home$', views.home, name='home'),
    url(r'^help$', views.manual, name='help'),
    url(r'^forum$', views.forum, name='forum'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^thanks$', views.thanks, name='thanks'),
    
    url(r'^immuno_app$', views.immuno_app, name='immuno_app'),
    url(r'^immuno_predict$', views.immuno_predict, name='immuno_predict'),
    url(r'^immuno_progress/(?P<task_id>[A-Za-z0-9-]+)$', views.immuno_progress, name='immuno_progress'),
    url(r'^immuno_results/(?P<task_id>[A-Za-z0-9-]+)$', views.immuno_results, name='immuno_results'),

    url(r'^feature_app$', views.feature_app, name='feature_app'),
    url(r'^feature_predict$', views.feature_predict, name='feature_predict'),
    url(r'^feature_progress/(?P<task_id>[A-Za-z0-9-]+)$', views.feature_progress, name='feature_progress'),
    url(r'^feature_results/(?P<task_id>[A-Za-z0-9-]+)$', views.feature_results, name='feature_results'),

]
