from django.urls import path

from cart import views

urlpatterns = [
    # 加入购物车
    path('add_cart/',views.add_cart, name='add_cart'),
    # 购物车数量的刷新
    path('cart_num/', views.cart_num, name='cart_num'),
    # 购物车
    path('cart/', views.cart, name='cart'),
    # 购物车价格
    path('cart_price/', views.cart_price, name='cart_price'),
#
    path('change_cart/',views.change_cart, name='change_cart'),
    path('del_cart/<int:id>/',views.del_cart, name='del_cart'),
    path('check_box/',views.check_box, name='check_box'),



]