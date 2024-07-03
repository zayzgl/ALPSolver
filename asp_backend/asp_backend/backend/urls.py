from django.urls import path, re_path
from . import views

urlpatterns = [
    path('user/login', views.login),
    path('user/info', views.getInfo),
    path('user/logout', views.logout),
    path('solve', views.solve),
    path('getcase', views.getCase),
]
