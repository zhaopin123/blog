import re

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from user.models import User, Browse


class AuthMiddleware(MiddlewareMixin):
     def process_request(self,request):


         user_id = request.session.get('user_id')
         if user_id:
             user = User.objects.filter(pk=user_id).first()
             request.user = user
         # 2.登陆校验，区分哪些地址需要登陆校验
         path = request.path
         if path == '/':
             return None
         not_need_chenk = ['/user/register/', '/user/login/',
                           '/goods/.*','/static/.*'
                           '/cart/.*/', '/media/.*',

                           ]
         for chenk_path in not_need_chenk:
             if re.match(chenk_path,path):
                 # 匹配上，不需要校验
                return None
         # 需要做登陆校验，没有登陆跳转登陆
         if not user_id:
             return HttpResponseRedirect(reverse('user:login'))

class SessionToDbMiddlewaer(MiddlewareMixin):
    def process_response(self,request,response):
        # 数据同步
        # 1.登陆才同步
        user_id = request.session.get('user_id')
        if user_id:
            # 2.同步
            # 判断session中商品是否在数据库，在则更新，无则创建
            session_browse = request.session.get('browse')
            if session_browse:
                for se_browse in session_browse:
                    br = Browse.objects.filter(br_id=se_browse,u_id=user_id).first()
                    if br:
                        
                        br.delete()
                    Browse.objects.create(br_id=se_browse,u_id=user_id)
                    session_browse.remove(se_browse)
                    brs = Browse.objects.filter(u_id=user_id)
                    if len(brs) > 5:
                        Browse.objects.first().delete()

            session_goods = request.session.get('goods')
            if session_goods:
                for se_goods in session_goods:
                    #         se_session: [goods_id, num, is_select]
                    cart = ShoppingCart.objects.filter(user_id=user_id,goods_id=se_goods[0]).first()
                    if cart:
                        # 更新信息
                        if cart.nums != se_goods[1] or cart.is_select != se_goods[2]:
                            cart.nums = se_goods[1]
                            cart.is_select = se_goods[2]
                            cart.save()
                    else:
                        # 创建
                        ShoppingCart.objects.create(
                            user_id=user_id,goods_id=se_goods[0],nums=se_goods[1],is_select=se_goods[2],
                        )

            # 同步数据库到session
            db_cart = ShoppingCart.objects.filter(user_id=user_id).all()
            # [[goods_id, num, is_select],[goods_id, num, is_select]]
            if db_cart:

                # [[cart.goods_id, cart.num, cart.is_select] for cart in db_cart]
                result = []
                for cart in db_cart:
                    data = [cart.goods_id, cart.nums, cart.is_select]
                    result.append(data)
                request.session['goods'] = result

        return response