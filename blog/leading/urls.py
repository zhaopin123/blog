from django.urls import path

from leading import views

urlpatterns = [

    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('gbook/', views.gbook,name='gbook'),
    path('info/<int:id>/', views.info, name='info'),
    path('infopic/', views.infopic, name='infopic'),
    path('share/', views.share, name='share'),
    path('list/', views.list, name='list'),
    path('search/',views.search, name='search'),
]