#Project-1\edusearch\edusearch\urls.py
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main_page'),
    path('search/', views.search_page, name='search_page'),
]
