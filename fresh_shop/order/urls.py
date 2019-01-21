from django.urls import path

from order import views

urlpatterns = [
    path('place_order/',views.place_order, name='place_order'),
    path('order/',views.order, name='order'),
    path('user_order/', views.user_order, name='user_order'),

]