from django.urls import path

from user import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('user_site/', views.user_site, name='user_site'),
    path('user_info/', views.user_info, name='user_info'),

]