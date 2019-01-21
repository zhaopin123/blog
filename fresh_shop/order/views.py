from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from cart.models import ShoppingCart
from fresh_shop.settings import ORDER_NUMBER
from order.models import OrderInfo, OrderGoods
from user.models import UserAddress
from utils.function import get_order_sn


def place_order(request):
    if request.method == 'GET':
        # 获取当前用户
        user = request.user
        carts = ShoppingCart.objects.filter(user=user,is_select=True).all()
        total_price = 0
        count = len(carts)

        for cart in carts:
            price = cart.goods.shop_price * cart.nums
            cart.goods_price = price
            total_price += price
        # 获取收获地址信息
        user_address = UserAddress.objects.filter(user=user).all()
        return  render(request, 'place_order.html',{'carts':carts,'total_price':total_price,'count':count,'user_address':user_address})

def order(request):
    if request.method == 'POST':

        # 1.获取id值
        ad_id = request.POST.get('ad_id')
        # 2.创建订单
        order_sn = get_order_sn()
        user_id = request.session.get('user_id')
        shop_cart = ShoppingCart.objects.filter(user_id=user_id,is_select=True)
        order_mount = 0
        for cart in shop_cart:
            order_mount += cart.goods.shop_price * cart.nums

        print(UserAddress.objects.filter(pk=ad_id).first())
        user_address = UserAddress.objects.filter(pk=ad_id).first()

        order = OrderInfo.objects.create(user_id=user_id,
                                 order_sn=order_sn,
                                 order_mount=order_mount,
                                 address=user_address.address,
                                 signer_name=user_address.signer_name,
                                 signer_mobile=user_address.signer_mobile

        )
        # 3.创建订单详情
        for cart in shop_cart:
            OrderGoods.objects.create(order=order,
                                      goods=cart.goods,
                                      goods_nums=cart.nums

            )
        # 4.删除购物车
        shop_cart.delete()
        session_goods = request.session.get('goods')
        for se_goods in session_goods:
            if se_goods[2]:
                session_goods.remove(se_goods)
        request.session['goods'] = session_goods
        return JsonResponse({'code':200,'msg':'成功',})

def user_order(request):
    if request.method == 'GET':
        page = int(request.GET.get('page',1))
        # 获取用户id
        user_id = request.session.get('user_id')
        orders = OrderInfo.objects.filter(user_id=user_id)
        status = OrderInfo.ORDER_STATUS
        pg = Paginator(orders, ORDER_NUMBER)
        orders = pg.page(page)
        act2 = 'order'
        return render(request,'user_center_order.html',{'orders':orders,'status':status,'act2':act2})
