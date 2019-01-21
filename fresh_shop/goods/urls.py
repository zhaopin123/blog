from django.urls import path

from goods import views

urlpatterns = [
    path('index/',views.index, name='index'),
    path('detail/',views.detail, name='detail'),
    path('by_price/',views.by_price, name='by_price'),
    path('by_click/',views.by_click, name='by_click'),
    path('list/',views.list, name='list'),
    path('search/',views.search, name='search'),
    path('detail/<int:id>/',views.detail,name='detail'),

]