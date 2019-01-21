from django.urls import path

from airtic import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('index/',views.index, name='index'),
    path('add_article/', views.add_article, name='add_article'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_flink/', views.add_flink, name='add_flink'),
    path('add_notice/', views.add_notice, name='add_notice'),
    path('article/', views.article, name='article'),
    path('category/', views.category, name='category'),
    path('comment/', views.comment, name='comment'),
    path('flink/',views.flink, name='flink'),
    path('loginlog/', views.loginlog, name='loginlog'),
    path('manage_user/', views.manage_user, name='manage_user'),
    path('notice/', views.notice, name='notice'),
    path('readset/', views.readset, name='readset'),
    path('setting/', views.setting, name='setting'),
    path('update_article/<int:id>/', views.update_article, name='update_article'),
    path('update_flink/', views.update_flink, name='update_flink'),
    path('update_category/<int:id>/', views.update_category, name='update_category'),
    path('del_art/<int:id>/', views.del_art, name='del_art'),
    path('del_lanmu/<int:id>/', views.del_lanmu, name='del_lanmu'),

]