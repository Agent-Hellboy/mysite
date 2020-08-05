from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('file/<str:name>/', views.fhandle, name='fhandler'),
    path('upload/', views.upload, name='upload'),
    path('teaminfo/', views.teaminfo, name='teaminfo'),
    path('team/', views.create_team, name='create_team'),
]
