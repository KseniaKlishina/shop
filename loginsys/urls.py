from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^order_basket/(?P<order>home|office)/$', 'loginsys.views.order'),        
     url(r'^order_one/(?P<type_order>home|office)/(?P<goods_id>\d+)/$', 'loginsys.views.order_one') ,
     url(r'^login/$', 'loginsys.views.login'),
     url(r'^logout/$', 'loginsys.views.logout'),
     url(r'^register/$', 'loginsys.views.register'),
     url(r'^account/$', 'loginsys.views.account'),
     url(r'^in_basket/(?P<good_id>\d+)/$', 'loginsys.views.in_busket'),
     url(r'^in_basket_to_basket/(?P<good_id>\d+)/', 'loginsys.views.in_basket_to_basket'),
     url(r'^basket/', 'loginsys.views.basket'),
     url(r'^change_password/(?P<activation_key>\w+)/$', 'loginsys.views.password_change'), 
    
      
     url(r'^change/$', 'loginsys.views.change_account'),
     url(r'^basket_goods_count_plus/(?P<goods_id>\d+)/$', 'loginsys.views.basket_goods_count_plus'),
     url(r'^basket_goods_count_minus/(?P<goods_id>\d+)/$', 'loginsys.views.basket_goods_count_minus'),
     url(r'^basket_delete/(?P<goods_id>\d+)/$', 'loginsys.views.basket_delete'),
     url(r'^buy/$', 'loginsys.views.buy'), 
)
 
