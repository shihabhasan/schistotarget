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
    url(r'^$', views.index, name='index'),
    url(r'^home$', views.home, name='home'),
    url(r'^help$', views.help, name='help'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^thanks$', views.thanks, name='thanks'),
    
    url(r'^immuno_app$', views.immuno_app, name='immuno_app'),
    url(r'^immuno_predict$', views.immuno_predict, name='immuno_predict'),
    url(r'^immuno_progress/(?P<task_id>[A-Za-z0-9-]+)$', views.immuno_progress, name='immuno_progress'),
    url(r'^immuno_results/(?P<task_id>[A-Za-z0-9-]+)$', views.immuno_results, name='immuno_results'),

    url(r'^IgE_app$', views.IgE_app, name='IgE_app'),
    url(r'^IgE_predict$', views.IgE_predict, name='IgE_predict'),
    url(r'^IgE_progress/(?P<task_id>[A-Za-z0-9-]+)$', views.IgE_progress, name='IgE_progress'),
    url(r'^IgE_results/(?P<task_id>[A-Za-z0-9-]+)$', views.IgE_results, name='IgE_results'),

    url(r'^IgG1_app$', views.IgG1_app, name='IgG1_app'),
    url(r'^IgG1_predict$', views.IgG1_predict, name='IgG1_predict'),
    url(r'^IgG1_progress/(?P<task_id>[A-Za-z0-9-]+)$', views.IgG1_progress, name='IgG1_progress'),
    url(r'^IgG1_results/(?P<task_id>[A-Za-z0-9-]+)$', views.IgG1_results, name='IgG1_results'),

    url(r'^IgG3_app$', views.IgG3_app, name='IgG3_app'),
    url(r'^IgG3_predict$', views.IgG3_predict, name='IgG3_predict'),
    url(r'^IgG3_progress/(?P<task_id>[A-Za-z0-9-]+)$', views.IgG3_progress, name='IgG3_progress'),
    url(r'^IgG3_results/(?P<task_id>[A-Za-z0-9-]+)$', views.IgG3_results, name='IgG3_results'),

    url(r'^IgG4_app$', views.IgG4_app, name='IgG4_app'),
    url(r'^IgG4_predict$', views.IgG4_predict, name='IgG4_predict'),
    url(r'^IgG4_progress/(?P<task_id>[A-Za-z0-9-]+)$', views.IgG4_progress, name='IgG4_progress'),
    url(r'^IgG4_results/(?P<task_id>[A-Za-z0-9-]+)$', views.IgG4_results, name='IgG4_results'),
]
