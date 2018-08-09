from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name = 'index'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.loginOut, name='logout'),
    path('calisan/ekle/', views.calisan_ekle, name = 'calisan_ekle'),
    path('gorev/ekle/', views.gorev_ekle, name = 'gorev_ekle'),
    path('gorev/sil/<int:gorev_id>',views.gorev_sil, name = 'gorev_sil'),
    path('gorev/liste/',views.gorev_liste, name = 'gorev_liste'),
    path('gorev/bitir/<int:gorev_id>', views.gorev_bitir, name = 'gorev_bitir'),
    path('gorev/gerigetir/<int:gorev_id>', views.gorev_geri_getir, name = 'gorev_geri_getir'),
    path('proje/ekle/', views.proje_ekle, name = 'proje_ekle'),
    path('proje/detay/<int:proje_id>', views.proje_detay, name = 'proje_detay'),
    path('proje/sil/<int:proje_id>', views.proje_sil, name = 'proje_sil'),
    path('calisan/ekle/', views.proje_ekle, name = 'calisan_ekle'),
    path('calisan/liste/',views.calisan_liste, name = 'calisan_liste'),
    path('gorev/ekle/', views.proje_ekle, name = 'gorev_ekle')
]