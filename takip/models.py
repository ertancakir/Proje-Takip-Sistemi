from django.db import models
from django import forms
from django.contrib.admin import widgets
import datetime


# Create your models here.


class Proje(models.Model):
    proje_id = models.AutoField(primary_key = True)
    proje_adi = models.CharField(max_length = 50)
    proje_baslama_tarih = models.DateField('Başlangıç Tarihi')
    proje_teslim_tarih = models.DateField('Bitiş Tarihi')

class Calisan(models.Model):
    calisan_id = models.AutoField(primary_key = True)
    calisan_adi = models.CharField(max_length = 10)
    calisan_soyadi = models.CharField(max_length = 10)
    calisan_yetki = models.CharField(max_length = 5)
    calisan_sifre = models.CharField(max_length = 10)
    calisan_email = models.CharField(max_length = 30)

class Gorev(models.Model):
    gorev_id = models.AutoField(primary_key = True)
    gorev_adi = models.CharField(max_length = 10)
    gorev_alan = models.ForeignKey(Calisan, on_delete = models.CASCADE, related_name = 'gorev_alan')
    gorev_veren = models.ForeignKey(Calisan, on_delete = models.CASCADE, related_name = 'gorev_veren')
    gorev_teslim_tarih = models.DateField('Son Teslim Tarihi')
    proje = models.ForeignKey(Proje, on_delete = models.CASCADE)
    gorev_durum = models.BooleanField(default=False)


class ProjeForm(forms.ModelForm):
    class Meta:
        model = Proje
        fields = ['proje_adi','proje_baslama_tarih', 'proje_teslim_tarih']
    def __init__(self, *args, **kwargs):
        super(ProjeForm, self).__init__(*args, **kwargs)
        self.fields['proje_adi'].widget = widgets.AdminTextInputWidget()
        self.fields['proje_baslama_tarih'].widget = widgets.AdminDateWidget()
        self.fields['proje_teslim_tarih'].widget = widgets.AdminDateWidget()

class CalisanForm(forms.ModelForm):
    class Meta:
        model = Calisan
        fields = ['calisan_adi','calisan_soyadi','calisan_email']
    def __init__(self, *args, **kwargs):
        super(CalisanForm, self).__init__(*args, **kwargs)
        self.fields['calisan_adi'].widget = widgets.AdminTextInputWidget()
        self.fields['calisan_soyadi'].widget = widgets.AdminTextInputWidget()
        self.fields['calisan_email'].widget = widgets.AdminEmailInputWidget()
    

class GorevForm(forms.Form):
    gorev_alan = forms.ModelChoiceField(queryset = Calisan.objects.all().values_list('calisan_adi',flat = True))
    gorev_veren = forms.ModelChoiceField(queryset = Calisan.objects.filter(calisan_yetki = 'admin').values_list('calisan_adi',flat = True))
    proje = forms.ModelChoiceField(queryset = Proje.objects.all().values_list('proje_adi',flat = True))

class LoginForm(forms.Form):
    email = forms.CharField(label = "Email")
    password = forms.CharField(label = "Şifre", widget = forms.PasswordInput)




