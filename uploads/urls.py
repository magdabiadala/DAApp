from django.conf.urls import url
from django.contrib import admin

from uploads.core import views


urlpatterns = [
    url('^$', views.home, name='home'),
    url('analiza_danych/', views.analiza_danych, name='analiza_danych'),
    url('o_nas/', views.o_nas, name='o_nas'),
    url('kontakt/', views.kontakt, name='kontakt'),
]
