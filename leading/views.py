from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from airtic.models import Article, LanMu
from leading.models import Gbook


def index(request):
    if request.method == 'GET':
        name = False
        if request.session.get('user_id'):
            name = True
        lanmu = LanMu.objects.all()
        arts = Article.objects.all()
        airs = arts[:8]
        page = int(request.GET.get('page', 1))
        pg = Paginator(arts, 6)
        arts = pg.page(page)
        return render(request,'index1.html',{'arts':arts,'name':name,'lanmu':lanmu,'airs':airs})


def list(request):
    if request.method == 'GET':
        act1 = True
        name = False
        if request.session.get('user_id'):
            name = True
        lanmu = LanMu.objects.all()
        page = int(request.GET.get('page', 1))
        arts = Article.objects.all()
        airs = arts[:8]
        pg = Paginator(arts, 8)
        arts = pg.page(page)
        return render(request, 'list.html',{'arts':arts,'lanmu':lanmu,'name':name,'airs':airs,'act1':act1})
    

def gbook(request):
    airs = Article.objects.all()[:8]

    lanmu = LanMu.objects.all()
    if request.method == 'GET':
        name = False
        if request.session.get('user_id'):
            name = True
        page = int(request.GET.get('page', 1))
        gbooks = Gbook.objects.all().order_by('-id')
        pg = Paginator(gbooks, 5)
        gbooks = pg.page(page)
        return render(request,'gbook.html',{'lanmu':lanmu,'gbooks':gbooks,'name':name,'airs':airs})
    if request.method == 'POST':

        name = request.POST.get('name')

        if name:
            gbook = Gbook()
            gbook.o_name = name
            gbook.cont = request.POST.get('lytext')
            gbook.email = request.POST.get('email')
            gbook.save()
            gbooks = Gbook.objects.all().order_by('-id')
            return render(request, 'gbook.html', {'lanmu': lanmu,'gbooks':gbooks,'airs':airs})

def about(request):

    if request.method == 'GET':
        airs = Article.objects.all()[:8]
        name = False
        if request.session.get('user_id'):
            name = True
        lanmu = LanMu.objects.all()
        return render(request,'about.html',{'lanmu':lanmu,'name':name,'airs':airs})



def info(request,id):
    if request.method == 'GET':
        airs = Article.objects.all()[:8]
        name = False
        if request.session.get('user_id'):
            name = True
        lanmu = LanMu.objects.all()
        art = Article.objects.filter(pk=id).first()
        return render(request,'info.html',{'art':art,'lanmu':lanmu,'name':name,'airs':airs})

def infopic(request):
    lanmu = LanMu.objects.all()

    return render(request,'infopic.html',{'lanmu':lanmu})


def share(request):
    lanmu = LanMu.objects.all()
    return render(request,'share.html',{'lanmu':lanmu})


def search(request):
    if request.method == 'GET':
        lanmu = LanMu.objects.all()
        keyword = request.session.get('keyword')
        key = keyword
        act =True
        page = int(request.GET.get('page', 1))
        airs = Article.objects.all()[:8]
        if LanMu.objects.filter(name__contains=keyword).first():
            lm = LanMu.objects.filter(name__contains=keyword).first()
            arts = Article.objects.filter(lm=lm.id).all()
        elif Article.objects.filter(key__contains=keyword).all():
            arts = Article.objects.filter(key__contains=keyword).all()
        elif Article.objects.filter(biaoqian__contains=keyword).all():
            arts = Article.objects.filter(biaoqian__contains=keyword).all()               
        else:
            arts = Article.objects.filter(title__contains=keyword).all()
        pg = Paginator(arts, 8)
        arts = pg.page(page)
        return render(request, 'list.html', {'arts': arts, 'lanmu': lanmu, 'key':key, 'airs':airs,})

    if request.method == 'POST':
        lanmu = LanMu.objects.all()
        keyword = request.POST.get('keyboard')
        key = ''
        act =True
        page = int(request.GET.get('page', 1))
        airs = Article.objects.all()[:8]
        if keyword:
            if LanMu.objects.filter(name__contains=keyword).first():
                lm = LanMu.objects.filter(name__contains=keyword).first()
                arts = Article.objects.filter(lm=lm.id).all()
                request.session['keyword'] = keyword
            elif Article.objects.filter(key__contains=keyword).all():
                arts = Article.objects.filter(key__contains=keyword).all()
                request.session['keyword'] = keyword
            elif Article.objects.filter(biaoqian__contains=keyword).all():
                arts = Article.objects.filter(biaoqian__contains=keyword).all()
                request.session['keyword'] = keyword
            elif Article.objects.filter(title__contains=keyword).all():
                arts = Article.objects.filter(title__contains=keyword).all()
                request.session['keyword'] = keyword
            else:

                arts = Article.objects.all()
                key = '没有 "' + keyword + '" 关键字'
        else:
            arts = Article.objects.all()
            key = '请输入关键字'
        pg = Paginator(arts, 8)
        arts = pg.page(page)
        return render(request, 'list.html', {'arts': arts, 'lanmu': lanmu, 'key':key, 'airs':airs,})

