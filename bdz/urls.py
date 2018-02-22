# -*- coding: utf-8 -*-
#from django.conf.urls import patterns, include, url
from django.conf.urls import  include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^confirm/(?P<activation_key>\w+)/$', 'loginsys.views.rest_register_confirm',name='rest_register_confirm'),
    url(r'^change-confirm/(?P<activation_key>\w+)/$', 'loginsys.views.change_confirm'),
    url(r'^auth/', include('loginsys.urls')),                   
    url(r'^$', 'website.views.home', name='home'),
    url(r'^contacts/$', 'website.views.contacts'),
    url(r'^(?P<category_name>texh|accessories|games)/$', 'website.views.cat', name='category_item'),                   
    url(r'^(?P<category_name>texh|accessories|games)/sub:(?P<subcategory_id>\d+)/org:(?P<org_id>\d+)/page:(?P<page>\d+):(?P<rating_or_price>rating|price)/$', 'website.views.subcate', name='org'),                   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^good/(?P<good_id>\d+)/$', 'website.views.good'),
    url(r'^events/(?P<events_id>\d+)/$', 'website.views.events'), 
    url(r'^search-/$', 'website.views.search'),
    url(r'^remember_password/$','loginsys.views.remember'),
    url(r'^change/(?P<activation_key>\w+)/$',  'loginsys.views.change'),                
            
]
