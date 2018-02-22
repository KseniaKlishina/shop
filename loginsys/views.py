# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response,redirect
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.shortcuts import render
from website.models import Category, City, Image, Organization,Country, CategoryImage, Goods, Delivery, GoodsCategories, Order, UserProfile, Basket
from django.core.mail import send_mail
from django.utils.datastructures import MultiValueDictKeyError
from django.core.signing import BadSignature
from django.contrib.auth.models import User
from django.http import Http404
import datetime
import re
from django.utils import timezone
import hashlib
import random
import sys
from smtplib import SMTPRecipientsRefused,SMTPDataError




def login (request):
  try: 
    args={}
    args['first_cat']=Category.objects.exclude(name__icontains='.')
    args['city_list']=City.objects.all()
    args.update(csrf(request))
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user=auth.authenticate(username=username, password=password)
        if user is not None and user.is_active==1:
            auth.login(request, user)
            return redirect('/auth/account/')
            
        else:
            args['login_error']="Неправильная комбинация логин-пароль!"
            return render(request,'login.html', args)
    else:
        return render(request, 'login.html', args) 
  except  :
        raise Http404


def logout(request):
  try:
    auth.logout(request)
    return redirect('/')
  except  :
        raise Http404

def key(user_email):
  salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
  activation_key = hashlib.sha1(salt+user_email).hexdigest()
  key_expires = datetime.datetime.today() + datetime.timedelta(3)
  return {'activation_key':activation_key, 'key_expires':key_expires}

def Send_mail_(email, email_subject, email_body, activation_key, key_expires):
           try:
               user=User.objects.get(email=email)
               
               
               send_mail(email_subject, email_body, 'angband_utumno@mail.ru',[user.email], fail_silently=False)
               new_profile=UserProfile.objects.get(user_id=user.id)
               new_profile.activation_key=activation_key
               new_profile.key_expires=key_expires
               new_profile.save()
               ok="На указанную Вами почту отправленно сообщение для изменения пароля"
               return ok
           except SMTPRecipientsRefused:
              context['email_error']="Почта не существует"
           except SMTPDataError:
              context['email_error']="Почта не существует"
  
def remember(request):
  try:
    context={}
    if request.POST:
        user_email=request.POST['email']
        user=User.objects.filter(email=user_email)
        if user.exists():
            user=User.objects.get(email=user_email)
            activation_key=key(user_email)['activation_key']
            key_expires=key(user_email)['key_expires']
            email_subject = 'Изменение пароля'
            email_body = "Hey %s. To change your password click the link http://127.0.0.1:8000/change/%s/" % (user.username, activation_key)
            context['ok']=Send_mail_(user.email, email_subject, email_body, activation_key, key_expires)
             
        else:
             context['email_error']="Такой пользователь не существует"
    return render(request, 'email.html', context)
  except  :
        raise Http404 
            

def password_change(request, activation_key):
  try:
    context={}
    if not request.user.is_authenticated() :
           new_profile=UserProfile.objects.filter(activation_key=activation_key)
           if not new_profile.exists():
              return redirect ('/auth/login/')
    context.update(csrf(request))
    context['key']=activation_key
    if request.POST:
        user_email=request.POST['email']
        password=request.POST['password_1']
        password_repeat=request.POST['password_2']
        if password==password_repeat and len(password)!=0:
            user = User.objects.filter(email=user_email)
            if user.exists() and len(user_email)!=0:
                user=User.objects.get(email=user_email)
                user.is_active=False
                user.set_password(password)
                user.save()
                activation_key=key(user_email)['activation_key']
                key_expires=key(user_email)['key_expires']
                email_subject = 'Изменение пароля'
                email_body = "Hey %s. To change your password click the link  http://127.0.0.1:8000/change-confirm/%s/" % (user.username, activation_key)
                context['ok']=Send_mail_(user.email, email_subject, email_body, activation_key, key_expires)
                   
               
            else:
                context['email_error']="Пользователь не найден"        
        else:
            context['password_error']="Пароли не совпадают"                 
    else:
        context['post']="post"
    return render_to_response('change_password.html', context)
  except  :
        raise Http404


      
def change(request, activation_key):
  try:
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    return redirect('/auth/change_password/'+activation_key)
  except  :
        raise Http404 

def change_confirm(request, activation_key):
 try:
    context={}
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
   
    user =user_profile.user
    user.is_active = True
    user.save()
    activation_key=key(user.email)['activation_key']
    key_expires=key(user.email)['key_expires']
    user_profile.activation_key=activation_key
    user_profile.save()
    return redirect('/auth/account/')
 except  :
        raise Http404 




def register(request):
  try:
    context={}    
    if request.user.is_authenticated():
        auth.logout(request)
    context.update(csrf(request))
    if request.POST:
       user_email=str(request.POST['email'])
       username=user_email
       password=request.POST['password_1']
       password_repeat=request.POST['password_2']
       email_check=User.objects.filter(email=user_email)       
       if email_check :
         context['email_error']="Такой пользователь уже существует"
         return render_to_response('register.html', context)          
       elif password==password_repeat and len(password)!=0:          
          user = User.objects.create_user(username, user_email, password)
          user.is_active=False
          user.save()          
          activation_key=key(user_email)['activation_key']
          key_expires=key(user_email)['key_expires']           
         
          email_subject = 'Подтверждение регистрации'
          email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \48hours http://127.0.0.1:8000/confirm/%s/" % (username, activation_key)
          try:
             send_mail(email_subject, email_body, 'angband_utumno@mail.ru',
                   [user_email], fail_silently=False)
             user=User.objects.get(username=user_email) 
             new_profile = UserProfile(user=user, activation_key=activation_key,key_expires=key_expires)
             new_profile.save()
             context['ok']="На указанную Вами почту отправленно сообщение для завершения регистрации"
          except SMTPRecipientsRefused:
              context['email_error']="Почта не существует"
          except SMTPDataError:
              context['email_error']="Почта не существует"
       else:
            context['password_error']="Пароли не совпадают"
    else:
        context['post']="post"
    return render_to_response('register.html', context)
  except  :
        raise Http404      
       
         
       
  
    


def rest_register_confirm(request, activation_key):
  try:
    context={}
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
   
    if user_profile.key_expires > timezone.now():
    
        context['key_arror']="Activate key is not valid"
        return redirect('/auth/register/', context)   
    user =user_profile.user
    user.is_active = True
    user.save()  
    return redirect('/auth/account/')
  except  :
        raise Http404











    
  


def account(request):
   try:
       context={}
       if not request.user.is_authenticated():
           return redirect ('/auth/login/')
       else:
           count_goods=0
           goods=Basket.objects.filter(user_id=request.user.id)
           
           for p in goods:
                   count_goods+=1
           perfect_good=[]          
           perfect_good=perfect_goods()         
           first_cat=Category.objects.exclude(name__icontains='.')
           city_list=City.objects.all()
           context['perfect_goods']=perfect_good
           context['user']=auth.get_user(request)
           context['city_list']=city_list
           context['first_cat']=first_cat
           context['count_goods']=count_goods
           context['account']=True
           return render(request, 'private_office.html',context) 
   except  :
        raise Http404

        

def in_busket(request, good_id):
    try:
       
        return_path  = request.META.get('HTTP_REFERER','/')
        response=redirect(return_path)
        if not request.user.is_authenticated():
            if good_id in request.session:
                request.session[good_id]=str(int(request.session[good_id].replace(str(auth.get_user(request).username),''))+1)
            else:    
               request.session.set_expiry(1209600)
               request.session[good_id] = str(auth.get_user(request).username)+'1'
        else:
            if Basket.objects.filter(user_id=request.user.id, goods_id=good_id):
              good=Basket.objects.get(user_id=request.user.id, goods_id=good_id)
              good.num_items=int(good.num_items)+1
              good.save()
            else:
              good=Basket(user_id=request.user, goods_id=Goods.objects.get(id=good_id), num_items=1, date=datetime.datetime.today())
              good.save()
        return response
    except  :
        raise Http404



def in_basket_to_basket(request, good_id):
  try:
        response=redirect('/auth/basket/')
        if not request.user.is_authenticated():
            if good_id in request.session:
                request.session[good_id]=str(int(request.session[good_id].replace( str(auth.get_user(request).username),''))+1)
            else:    
                request.session.set_expiry(1209600)
                request.session[good_id] = str(auth.get_user(request).username)+'1'
        else:
                if Basket.objects.filter(user_id=request.user.id, goods_id=good_id):
                    good=Basket.objects.get(user_id=request.user.id, goods_id=good_id)
                    good.num_items=int(good.num_items)+1
                    good.save()
                else:
                    good=Basket(user_id=request.user, goods_id=Goods.objects.get(id=good_id), num_items=1, date=datetime.datetime.today())
                    good.save()
        
        return response
  except  :
        raise Http404
 
  
       
def basket_goods_count_plus(request, goods_id):
  try:
     if not request.user.is_authenticated():
         request.session[goods_id]=str(int(request.session[goods_id].replace(auth.get_user(request).username,''))+1)
     else:
          good=Basket.objects.get(user_id=request.user.id, goods_id=goods_id)
          good.num_items=int(good.num_items)+1
          good.save()
     return redirect('/auth/basket/')
  except  :
        raise Http404


def basket_goods_count_minus(request, goods_id):
  try:
    if not request.user.is_authenticated():
        if int(request.session[goods_id].replace(auth.get_user(request).username,''))>1:
            request.session[goods_id]=str(int(request.session[goods_id].replace(auth.get_user(request).username,''))-1)
    else:
          good=Basket.objects.get(user_id=request.user.id, goods_id=goods_id)
          if int(good.num_items)>1:
             good.num_items=int(good.num_items)-1
             good.save()
      
    return redirect('/auth/basket/')
  except  :
        raise Http404 



def basket_delete(request, goods_id):
  try:
     if not request.user.is_authenticated():
        del request.session[goods_id]
     else:
        
       good=Basket.objects.get(user_id=request.user.id, goods_id=goods_id)
       good.delete()
     return redirect('/auth/basket/')
  except  :
        raise Http404



def basket(request):
  try: 
    context={}
    good=[]
    count={}
    if not request.user.is_authenticated():
        for p in request.session.keys():
            if p.isdigit():
                d=int(p)
                good.append(Goods.objects.get(id=d))
                count[d]=request.session[p].replace(str(auth.get_user(request).username),'')
        context['mas']=good
        context['count']=count

        goods=Basket.objects.filter(user_id=request.user.id)
        
        context['goods']=goods
    city_list=City.objects.all()
    first_cat=Category.objects.exclude(name__icontains='.')
    perfect_good=perfect_goods()
   
    context['perfect_goods']=perfect_good
    context['first_cat']=first_cat
    context['city_list']=city_list
    
    
   
    return render(request, 'basket.html',context )
  except  :
        raise Http404





def order_one(request,type_order, goods_id):
  try:  
    
    context={}
    context['num_error']=False
    context['phone_error']=False
    context['adress_error']=False
    context['type']=type_order
    context['good']=Goods.objects.get(id=goods_id)
    context['summ']=Goods.objects.get(id=goods_id).price
    context['city_list']=City.objects.all()
    context['first_cat']=first_cat=Category.objects.exclude(name__icontains='.')
    context['one']=True
    if request.POST:
        try:
            adress = request.POST['adress']
        except MultiValueDictKeyError:
            adress=0
        telephone=str(request.POST['telephone']).encode('utf-8') 
        use_name=request.POST['use_name']
        town=request.POST['town']
        if re.search('^\d-\d\d\d-\d\d\d-\d\d-\d\d$', telephone) is None:
                    context['phone_error']='введите правильный номер!'
      
        if  type_order == "home":
                if len(adress)==0:
                    context['adress_error']="введите адрес"
            
        if (context['num_error']!=False) or (context['phone_error']!=False) or (context['adress_error']!=False):
            return render(request, 'order.html', context)
        else:
           num = random.randint(1000000,99999999)
           while Order.objects.filter(num_order=num):
              num = random.randint(1000000,99999999)
           if not request.user.is_authenticated():
                 for p in request.session.keys():
                    if p.isdigit():
                       d=int(p)  
                  
                       b=Order(num_order=num, goods_id=Goods.objects.get(id=d), city_id=City.objects.get(name=town), num_items=request.session[p],
                          use_name=use_name, telephones=telephone, adress=adress)
                       b.save()
                       del request.session[p]
                 context['ok']="Ваш заказ принят"
                 return render(request, 'register.html', context) 
           else:
                   basket=Basket.objects.filter(user_id=request.user.id)
                   for p in basket:
                      b=Order(num_order=num, goods_id=Goods.objects.get(id=p.id), city_id=City.objects.get(name=town), num_items=p.num_items,
                          use_name=use_name, telephones=telephone, adress=adress, user_id=request.user)
                      b.save()
                      Basket.delete(p)
                  
                   return redirect('/auth/buy')
   
    return render(request, 'order.html', context)
  except  :
        raise Http404


   
def order(request, order):
  try:
    my_good=[]
    context={}
    count={}
    summ=0
    if not request.user.is_authenticated():
        for p in request.session.keys():
           if p.isdigit():
              d=int(p)
              my_good.append(Goods.objects.get(id=d))
              count[d]=request.session[p].replace(auth.get_user(request).username,'')
              summ+=int(count[d])*int(Goods.objects.get(id=d).price)
        context['mas']=my_good 
    else:
      good=Basket.objects.filter(user_id=request.user.id)
      context['mas']=good 
      for p in good:
        summ+=int(p.goods_id.price)*int(p.num_items)
    context['city_list']=City.objects.all()
    context['count']=count
    context['summ']=summ
    context['first_cat']=first_cat=Category.objects.exclude(name__icontains='.')
     
    context['phone_error']=False
    context['adress_error']=False
    context['type']=order
    if request.POST:
        try:
            adress = request.POST['adress']
        except MultiValueDictKeyError:
            adress=0
        telephone=str(request.POST['telephone']).encode('utf-8') 
        use_name=request.POST['use_name']
        town=request.POST['town']
        if re.search('^\d-\d\d\d-\d\d\d-\d\d-\d\d$', telephone) is None:
                    context['phone_error']='введите правильный номер!'
      
        if  order == "home":
                if (len(adress)==0):
                    context['adress_error']="введите адрес"
            
        if   (context['phone_error']!=False) or (context['adress_error']!=False):
            return render(request, 'order.html', context)
        else:
             num = random.randint(1000000,99999999)
             while Order.objects.filter(num_order=num):
                      num = random.randint(1000000,99999999)
             if not request.user.is_authenticated():
                 for p in request.session.keys():
                    if p.isdigit():
                       d=int(p)  
                  
                       b=Order(num_order=num, goods_id=Goods.objects.get(id=d), city_id=City.objects.get(name=town), num_items=request.session[p],
                          use_name=use_name, telephones=telephone, adress=adress)
                       b.save()
                       del request.session[p]
                 context['ok']="Ваш заказ принят"
                 return render(request, 'register.html', context) 
             else:
                   basket=Basket.objects.filter(user_id=request.user.id)
                   for p in basket:
                      b=Order(num_order=num, goods_id=Goods.objects.get(id=p.id), city_id=City.objects.get(name=town), num_items=p.num_items,
                          use_name=use_name, telephones=telephone, adress=adress, user_id=request.user)
                      b.save()
                      Basket.delete(p)
                  
                   return redirect('/auth/buy')
               
    return render(request, 'order.html', context)
  except  :
        raise Http404


 




                
def buy(request):
 try:  
    if not request.user.is_authenticated():
           return redirect ('/auth/login/')
    first_cat=Category.objects.exclude(name__icontains='.')
    city_list=City.objects.all() 
    buy=Order.objects.filter(user_id=request.user.id)
    persect_good=[]
    perfect_good=perfect_goods()   
    context={'buy':buy,'first_cat':first_cat, 'city_list':city_list, 'perfect_goods':perfect_good   }
    return render(request, 'buy.html', context)
 except  :
        raise Http404
    


def change_account(request):
 try:  
    if not request.user.is_authenticated():
           return redirect ('/auth/login/')
    if request.POST:
        name=request.POST['name']
        sename=request.POST['sename']
        username=request.POST['username']
        if len(username)!=0:
            request.user.username=username
        if len(sename)!=0:
            request.user.last_name=sename
        if len(name)!=0:
            request.user.first_name=name
        request.user.save()
        return redirect('/auth/account/')
    return render(request, 'change.html')
 except  :
       raise Http404
            
def perfect_goods():
   second_cat=Category.objects.filter(name__icontains='.').order_by('?')[:4]   
   mas=[]
   for p in second_cat:
          m=GoodsCategories.objects.filter(category_id=p.id)
          if m.exists():
                  mas.append(m.order_by('goods_id__rating').reverse()[0])
  
   mas=mas[:4]
   return mas
   

          
    
