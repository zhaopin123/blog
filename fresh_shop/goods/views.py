from django.core.paginator import Paginator
from django.shortcuts import render

from goods.models import GoodsCategory, Goods
from user.models import Browse


def index(request):
    if request.method == 'GET':
        # 分类,该分类前四个商品
        # 1.category_name:[object1,object2,object3,object4]
        categorys =  GoodsCategory.objects.all()
        result = []
        for category in categorys:
            goods = category.goods_set.all()[:4]
            data = [category,goods]
            result.append(data)
        category_type = GoodsCategory.CATEGORY_TYPE
        return render(request, 'index.html',{'result':result,'category_type':category_type})

    if request.method == 'POST':
        pass


def list(request):
    if request.method == 'GET':
        act = True
        page = int(request.GET.get('page', 1))
        sea = request.session.get('search')
        if sea:
            type = GoodsCategory.objects.filter(ty_name__contains=sea).first()
            if type:
                goods = Goods.objects.filter(category=type.id).all()

            elif Goods.objects.filter(name__contains=sea).all():
                goods = Goods.objects.filter(name__contains=sea).all()
            else:

                goods = Goods.objects.all()
        else:
            goods = Goods.objects.all()
        pg = Paginator(goods, 15)
        goods = pg.page(page)
        return render(request, 'list.html',{'goods':goods,'act':act})


def detail(request,id):
    if request.method == 'GET':
        goods = Goods.objects.filter(pk=id).first()
        goods.click_nums += 1
        goods.save()
        session_browse = request.session.get('browse')
        if session_browse:
            for se_browse in session_browse:
                if se_browse == id:
                    session_browse.remove(se_browse)
                session_browse.append(id)

        else:
            request.session['browse'] = [id]
        session_goods = request.session.get('goods')
        num = 1
        all_price = goods.shop_price
        if session_goods:
            for se_goods in session_goods:
                if se_goods[0] == id:
                    num = se_goods[1]
                    all_price = goods.shop_price * num
        return render(request,'detail.html',{'goods':goods,'num':num,'all_price':all_price})


def search(request):
    if request.method == 'GET':
        act = True
        search = request.session.get('search')
        page = int(request.GET.get('page', 1))
        type = GoodsCategory.objects.filter(ty_name__contains=search).first()
        key = search
        if type:
            goods = Goods.objects.filter(category=type.id).all()
        else:
            goods = Goods.objects.filter(name__contains=search).all()
        pg = Paginator(goods, 15)
        goods = pg.page(page)
        return render(request, 'list.html', {'goods': goods, 'key': key, 'act1': act})
    if request.method == 'POST':
        act = True
        page = int(request.GET.get('page', 1))
        goods = Goods.objects.all()
        search = request.POST.get('search')

        key = ''
        if search:
            type = GoodsCategory.objects.filter(ty_name__contains=search).first()
            if type:
                goods = Goods.objects.filter(category=type.id).all()

                request.session['search'] = search
                key = search
            elif Goods.objects.filter(name__contains=search).all():
                goods = Goods.objects.filter(name__contains=search).all()

                request.session['search'] = search
                key = search
            else:
                key = '没有 "' + search + '" 关键字'
        else:
            key = '没有 "' + search + '" 关键字'
        pg = Paginator(goods, 15)
        goods = pg.page(page)
        return render(request, 'list.html',{'goods':goods,'key':key,'act1':act})

def by_price(request):
    if request.method == "GET":
        act = True
        page = int(request.GET.get('page', 1))
        sea = request.session.get('search')
        if sea:
            type = GoodsCategory.objects.filter(ty_name__contains=sea).first()
            if type:
                goods = Goods.objects.filter(category=type.id).all().order_by('-shop_price')

            elif Goods.objects.filter(name__contains=sea).all():
                goods = Goods.objects.filter(name__contains=sea).all().order_by('-shop_price')
            else:

                goods = Goods.objects.all().order_by('-shop_price')
        else:
            goods = Goods.objects.all().order_by('-shop_price')
        pg = Paginator(goods, 15)
        goods = pg.page(page)
        return render(request, 'list.html', {'goods': goods,'act2':act})


def by_click(request):
    if request.method == "GET":
        act = True
        page = int(request.GET.get('page', 1))
        sea = request.session.get('search')
        if sea:
            type = GoodsCategory.objects.filter(ty_name__contains=sea).first()
            if type:
                goods = Goods.objects.filter(category=type.id).all().order_by('-click_nums')

            elif Goods.objects.filter(name__contains=sea).all():
                goods = Goods.objects.filter(name__contains=sea).all().order_by('-click_nums')
            else:

                goods = Goods.objects.all().order_by('-click_nums')
        else:

            goods = Goods.objects.all().order_by('-click_nums')
        pg = Paginator(goods, 15)
        goods = pg.page(page)
        return render(request, 'list.html', {'goods': goods,'act3':act})