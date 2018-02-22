# -*- coding: utf-8 -*-
from django.core.files import File
from django.shortcuts import render, redirect, render_to_response
from website.models import Category, City, Image, Organization,Country,Advertising, Events, CategoryImage, Goods, Delivery, GoodsCategories, Contacts
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from django.template import TemplateDoesNotExist
from django.http import Http404
from django.http import HttpResponse
from django.core.signing import BadSignature
from bdz.settings import MEDIA_ROOT
import sys 



def home(request):
    try:  
        city_list=City.objects.all()
        category=CategoryImage.objects.all()
        banner=Advertising.objects.all().last()
        events=Events.objects.order_by('pub_date')[:3]
        first_cat=Category.objects.exclude(name__icontains='.')
        my={}
        for_lis_box={}
        for p in first_cat:
            value=Category.objects.filter(name__icontains=p.name+'.')
            for t in value:
                S=t.name
                st=S.split('.')[0]+'.'+S.split('.')[1]+'.'


                
                value=value.exclude(name__icontains=st)
            my[p.name]=value
                         
        for p in category:
            if p.category_id.name.find('.')!= -1:
                s=p.category_id.name.split('.')
                for_lis_box[p.category_id.title]=s[0]
            else: for_lis_box[p.category_id.title]=p.name        
            
        context = { 'city_list':city_list,  'category': category, 'banner':banner, 'events':events, 'first_cat':first_cat, 'my':my, 'for_lis_box':for_lis_box}
        return render(request, 'home.html', context)
    except  :
        raise Http404
  
        


       
        
    
def cat(request,category_name):
    try:    
        short_description={}
        count=[]
        for i in range(1,100,3):
            count.append(i)
        first_cat=Category.objects.exclude(name__icontains='.')
        city_list=City.objects.all()
        title=Category.objects.get(name=category_name)
        second_cat=Category.objects.filter(name__icontains=category_name+'.')
        names=[]
        for p in second_cat:
            head=GoodsCategories.objects.filter(category_id=p.id)
            if head.exists():
                names.append(head.order_by('goods_id__rating').reverse()[0])
  
   
        for p in names:
            S=p.category_id.name
            head =S.split('.')
            st=S.split('.')[0]+'.'+S.split('.')[1]+'.'
            for values in names:
                if  values.category_id.name.find(st)!=-1 and p!=values:
                    if int(values.goods_id.rating)>=int(p.goods_id.rating):
                        names.remove(p)
                    else :
                        names.remove(values) 
            second_cat=second_cat.exclude(name__icontains=st)
        for p in names:
            short_description[p.goods_id.id]=p.goods_id.description[:200]+'...'
           
        context= {'city_list':city_list, 'first_cat':first_cat,'title':title, 'second_cat':second_cat,'mas':names,'count':count ,'short_description':short_description,   }
        return render(request, 'category.html', context)
    except  :
        raise Http404



def subcate(request, category_name, subcategory_id, org_id, page, rating_or_price ):
   try:
      nomber_goods_on_page=5
      first_cat=Category.objects.exclude(name__icontains='.')
      city_list=City.objects.all()
      subcategoryes=Category.objects.get(id=subcategory_id)   
      if org_id=='0':
          list_goods=GoodsCategories.objects.filter(category_id=subcategory_id)
      else:
          list_goods=GoodsCategories.objects.filter(category_id=subcategory_id, goods_id__organization_id=org_id)
      list_org=GoodsCategories.objects.filter(category_id=subcategory_id).values('goods_id__organization_id__title','goods_id__organization_id').distinct()    
      title=Category.objects.get(name=category_name)
      banner=Advertising.objects.all().last()
      count=list_goods.count()
      if count%5>0:
          count=count/nomber_goods_on_page+1
      else: count=count/nomber_goods_on_page
      pag=int(page)   
      if pag<1:
          pag=1
          prev=1      
      else:
          prev=pag-1
      if pag>count:
         pag=count
         prev=count-1
      a=(pag-1)*nomber_goods_on_page
      b=a+nomber_goods_on_page
      if list_goods.exists():
          if rating_or_price == "rating":
              list_goods=list_goods.order_by('goods_id__rating').reverse()[a:b]
          if rating_or_price == "price":
              list_goods=list_goods.order_by('goods_id__price')[a:b]
      pages=[]
      if  pag-nomber_goods_on_page/2>0:
        range1=pag-nomber_goods_on_page/2
      else:
          range1=1
      range2=range1+5
      if range2>count+1:
          range2=count+1
    
      for i in range(range1, range2):      
          
              pages.append(i)
              i=+1
      str_for_rating={}
      for p in list_goods:
          str_for_rating[p.goods_id.id]='.'*int(p.goods_id.rating)
      Context= {'subcategoryes':subcategoryes, 'title':title,'org_id':int(org_id), 'city_list':city_list, 'list_org':list_org,
             'rating_or_price':rating_or_price, 'pages':pages,'str_for_rating':str_for_rating,  'page':pag, 'prev':prev, 'next':pag+nomber_goods_on_page, 'list_goods':list_goods,
             'first_cat':first_cat,'banner':banner}
      return render(request, 'subcategory.html', Context)
   except  :
        raise Http404
  



def good(request, good_id):
    try:    
        good=Goods.objects.get(id=good_id)
        city_list=City.objects.all()
        rating='s'*good.rating
        first_cat=Category.objects.exclude(name__icontains='.')
        Context={'city_list':city_list,'first_cat':first_cat,  'good':good,'rating':rating}
        return render(request, 'article.html', Context)
    except  :
        raise Http404

import codecs
def events(request, events_id):
     try:   
        city_list=City.objects.all()
        first_cat=Category.objects.exclude(name__icontains='.')
        event=Events.objects.get(id=events_id)
        file_=open(MEDIA_ROOT+str(Events.objects.get(id=events_id).contents),'r')
        #file_.write(codecs.BOM_UTF8)
        article=str(file_.read())
      
        file_.close()
        Context={'city_list':city_list,'first_cat':first_cat, 'str':article, 'event':event
                 }
        return render(request, 'event.html', Context)
     except  :
        raise Http404



def search(request):
    try:           
       context={}
       context.update(csrf(request))
       if request.POST:
           first_cat=Category.objects.exclude(name__icontains='.')              
           names={}             
           for p in first_cat:
               value=Category.objects.filter(name__icontains=p.name+'.')
               for t in value:
                   S=t.name
                   st=S.split('.')[0]+'.'+S.split('.')[1]+'.'
                   value=value.exclude(name__icontains=st)
               names[p.name]=value
           context['my']=names  
           city_list=City.objects.all()  
           search= request.POST['search_good']
           town=request.POST['town']
           good_1=Delivery.objects.filter(city_id__name=town, goods_id__title__icontains=search)
           good_2=Delivery.objects.filter(city_id__name=town, goods_id__title__contains=search.capitalize())
           good=good_1|good_2
           adress=str(request.path)
           context['good']=good
           context['city_list']=city_list
           context['first_cat']=first_cat
           context['search']=search
           str_for_rating={}
           for p in good:
                 str_for_rating[p.goods_id.id]='.'*int(p.goods_id.rating)
           context['str_for_rating']=str_for_rating
           context['banner']=Advertising.objects.all().last()
           return render_to_response('search.html', context)              
       else :
           return HttpResponse("Ошибка!")
    except  :
        raise Http404 

                
        
def contacts(request):
  try:
        first_cat=Category.objects.exclude(name__icontains='.')
        city_list=City.objects.all()
        contacts=Contacts.objects.all()
        Context={'city_list':city_list,'first_cat':first_cat,'contacts':contacts}
        return render(request, 'contacts.html', Context)
  except :
        raise Http404
        

