from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from airtic.forms import LoginForm
from airtic.models import User, Article, LanMu


def login(request):
    if request.method == 'GET':
        request.session.flush()
        return render(request, 'login.html')
    if request.method == 'POST':
        # 获取登录提交的参数
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('leading:index'))
        else:
            msg = '账号或密码错误'
            return render(request, 'login.html', {'msg': msg})

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        # 1. 接收页面中传递的参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # 2. 实现保存用户信息到user表中
        if User.objects.filter(username=username).exists():
            msg = '账号已存在'
            return render(request, 'register.html', {'msg': msg})
        if password != password2:
            msg = '密码不一致'
            return render(request, 'register.html', {'msg': msg})
        password = make_password(password)
        User.objects.create(username=username, password=password)
        # 3. 跳转到登录
        return HttpResponseRedirect(reverse('airtic:login'))

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

def article(request):
    if request.method == 'GET':

        page = int(request.GET.get('page', 1))
        arts = Article.objects.all()
        pg = Paginator(arts, 5)
        arts = pg.page(page)
        return render(request, 'article.html', {'arts': arts})

def del_art(request,id):
    if request.method == 'GET':
        Article.objects.filter(pk=id).delete()
        return HttpResponseRedirect(reverse('airtic:article'))



def add_article(request):
    if request.method == 'GET':
        lanmu = LanMu.objects.all()
        print(lanmu)
        return render(request, 'add_article.html',{'lanmu':lanmu})
    if request.method == 'POST':
        title = request.POST.get('title')
        icon = request.FILES.get('icon')
        data = request.POST.get('content')
        biaoqian = request.POST.get('biaoqian')
        lm_id = request.POST.get('category')
        key = request.POST.get('keywords')
        miaoshu = request.POST.get('describe')
        Article.objects.create(
            title=title,
            icon=icon,
            data=data,
            biaoqian=biaoqian,
            lm_id=lm_id,
            key=key,
            miaoshu=miaoshu
        )
        return HttpResponseRedirect(reverse('airtic:article'))

def add_category(request):
    if request.method == 'GET':
        return render(request, 'add_category.html')

def add_flink(request):
    if request.method == 'GET':
        return render(request, 'add_flink.html')

def add_notice(request):
    if request.method == 'GET':
        return render(request, 'add_notice.html')

def category(request):
    if request.method == 'GET':
        lanmus = LanMu.objects.all()
        return render(request, 'category.html',{'lanmus':lanmus})
    if request.method == 'POST':
        lm = LanMu()
        lm.name = request.POST.get('name')
        lm.other_name = request.POST.get('alias')
        lm.keyword = request.POST.get('keywords')
        lm.mshu = request.POST.get('describe')
        lm.save()
        return HttpResponseRedirect(reverse('airtic:category'))

def del_lanmu(request,id):
    if request.method == 'GET':
        LanMu.objects.filter(pk=id).delete()
        return HttpResponseRedirect(reverse('airtic:category'))

def comment(request):
    if request.method == 'GET':
        return render(request, 'comment.html')
def flink(request):
    if request.method == 'GET':
        return render(request, 'flink.html')
def loginlog(request):
    if request.method == 'GET':
        return render(request, 'loginlog.html')
def manage_user(request):
    if request.method == 'GET':
        return render(request, 'manage_user.html')
def notice(request):
    if request.method == 'GET':
        return render(request, 'notice.html')
def readset(request):
    if request.method == 'GET':
        return render(request, 'readset.html')
def setting(request):
    if request.method == 'GET':
        return render(request, 'setting.html')
def update_article(request,id):
    if request.method == 'GET':
        lanmu = LanMu.objects.all()
        art = Article.objects.filter(pk=id).first()
        return render(request, 'update_article.html', {'art': art,'lanmu':lanmu})
    if request.method == 'POST':
        art = Article.objects.filter(pk=id).first()
        art.title = request.POST.get('title')
        art.icon = request.FILES.get('icon')

        art.data = request.POST.get('content')
        art.biaoqian = request.POST.get('biaoqian')
        art.lm_id = request.POST.get('category')
        art.key = request.POST.get('keywords')
        art.miaoshu = request.POST.get('describe')
        art.save()

        return HttpResponseRedirect(reverse('airtic:article'))

def update_category(request,id):
    if request.method == 'GET':
        lanmus = LanMu.objects.all()
        lanmu = LanMu.objects.filter(pk=id).first()
        return render(request, 'update_category.html', {'lanmu': lanmu, 'lanmus':lanmus})
    if request.method == 'POST':
        lm = LanMu.objects.filter(pk=id).first()
        lm.name = request.POST.get('name')
        lm.other_name = request.POST.get('alias')
        lm.keyword = request.POST.get('keywords')
        lm.mshu = request.POST.get('describe')
        lm.save()
        return HttpResponseRedirect(reverse('airtic:category'))

def update_flink(request):
    if request.method == 'GET':
        return render(request, 'update_flink.html')
