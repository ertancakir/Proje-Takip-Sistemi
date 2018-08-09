from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login as auth_login , logout
import datetime
from django.core import serializers


from .models import ProjeForm, CalisanForm, GorevForm, LoginForm, Calisan, Proje, Gorev


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        calisan = Calisan.objects.filter(calisan_adi = request.user)
        gorevler = Gorev.objects.filter(gorev_alan = calisan[0])
        projeler = Proje.objects.all()
        return render(request, 'takip/index.html',{'calisan':calisan[0],'gorevler':gorevler,'projeler':projeler})
    else:
        return redirect('/takip/login/')


def login(request):
    if request.method == 'POST':
        uname = request.POST.get('email','')
        upass = request.POST.get('password','')
        user = authenticate(request, username=uname, password=upass)
        if user is not None:
            auth_login(request,user)
            return redirect('/takip/index/')
        else:
            return redirect('/takip/login/')

    else:
        login_form = LoginForm()
        return render(request, 'takip/login.html',{'form':login_form})

def loginOut(request):
    logout(request)
    return redirect('/takip/login/')

def calisan_ekle(request):
    if request.method == 'POST':
        c = Calisan()
        c.calisan_sifre = request.POST.get('calisan_sifre','')
        c.calisan_yetki = request.POST.get('calisan_yetki','')
        cf = CalisanForm(request.POST,instance = c)
        yeni_calisan = cf.save()
        user = User.objects.create_user(username = yeni_calisan.calisan_adi, email= yeni_calisan.calisan_email, password=yeni_calisan.calisan_sifre)
        return redirect('/takip/index/')
    else:
        calisan_form = CalisanForm()
        return render(request, 'takip/calisan_ekle.html',{'form':calisan_form})

def calisan_liste(request):
    c = Calisan.objects.all().order_by('calisan_yetki')
    return render(request,'takip/calisan_liste.html',{'calisanlar':c})

def gorev_ekle(request):
    if request.method == 'POST':
        gf = GorevForm()
        gorev = Gorev()
        gorev_veren = Calisan.objects.filter(calisan_adi = request.POST.get('gorev_veren',''))
        gorev_alan = Calisan.objects.filter(calisan_adi = request.POST.get('gorev_alan',''))
        proje = Proje.objects.filter(proje_adi = request.POST.get('proje',''))

        gorev.gorev_veren = gorev_veren[0]
        gorev.gorev_alan = gorev_alan[0]
        gorev.proje = proje[0]
        gorev.gorev_adi = request.POST.get('gorev_adi','')
        gorev.gorev_teslim_tarih = request.POST.get('gorev_teslim_tarih','')
        gorev.save()
        return redirect('/takip/index/')
    else:
        c = Calisan.objects.filter(calisan_adi = request.user)
        if c[0].calisan_yetki == 'admin':
            gorev_form = GorevForm()
            return render(request, 'takip/gorev_ekle.html',{'form':gorev_form})
        else:
            return redirect('/takip/index/')

def gorev_bitir(request, gorev_id):
    gorev = Gorev.objects.filter(pk = gorev_id).update(gorev_durum = True)

    return redirect('/takip/index/')

def gorev_geri_getir(request, gorev_id):
    gorev = Gorev.objects.filter(pk = gorev_id).update(gorev_durum = False)
    return redirect('/takip/index/')

def gorev_liste(request):
    gorev = Gorev.objects.all()
    return render(request,'takip/gorev_liste.html',{'gorevler':gorev})


def proje_ekle(request):
    if request.method == 'POST':
        p = Proje()
        p.proje_adi = request.POST.get('proje_adi','')
        p.proje_baslama_tarih = request.POST.get('proje_baslama_tarih','')
        p.proje_teslim_tarih = request.POST.get('proje_teslim_tarih','')
        p.save()
        return redirect('/takip/index/')
    else:
        proje_form = ProjeForm()
        return render(request, 'takip/proje_ekle.html',{'form':proje_form})

def proje_sil(request, proje_id):
    proje = Proje.objects.get(pk = proje_id)
    proje.delete();
    return redirect('/takip/index/')


def proje_detay(request, proje_id):
    p = Proje.objects.filter(pk = proje_id)
    gorevler = Gorev.objects.filter(proje = p[0])
    return render(request, 'takip/proje_detay.html',{ 'gorevler':gorevler , 'proje_adi':p[0].proje_adi})

def gorev_sil(request, gorev_id):
    gorev = Gorev.objects.get(pk = gorev_id)
    gorev.delete()
    return redirect('/takip/index/')
    