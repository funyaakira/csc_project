from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class MT_SEX(models.Model):
    def __str__(self):
        return self.SEX
    SEX = models.CharField(max_length=200)

class MT_EVENT_KND(models.Model):
    def __str__(self):
        return self.EV_KND_NAME
    EV_KND_NAME = models.CharField(max_length=200)

class MT_HC_KND(models.Model):
    def __str__(self):
        return self.HC_KND_NAME
    HC_KND_NAME = models.CharField(max_length=200)

class MT_GAIBU(models.Model):
    def __str__(self):
        return self.GB_NAME
    GB_NAME = models.CharField(max_length=200)

class MT_SYOKUMU(models.Model):
    def __str__(self):
        return self.SYOKUMU_NAME
    SYOKUMU_NAME = models.CharField(max_length=200, null=True)

class MT_STAFF(models.Model):
    def __str__(self):
        return self.STAFF_NAME
    USER = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    SYOKUMU_ID = models.ForeignKey(MT_SYOKUMU, on_delete=models.CASCADE)
    STAFF_NAME = models.CharField(max_length=200, null=True)
    DEL_FLG = models.BooleanField(default=False)

class DT_RIYOSYA(models.Model):
    def __str__(self):
        return self.NAME
    NAME = models.CharField(max_length=200)
    FURIGANA = models.CharField(max_length=200)
    SEX = models.ForeignKey(MT_SEX,on_delete=models.PROTECT,default=0)
    BIRTH_DAY = models.DateField(null=True,default=None)
    DEL_FLG = models.BooleanField(default=False)


class DT_EVENT(models.Model):
    def __str__(self):
        return str(self.EV_DATE.strftime("%Y/%m/%d")) + " " + str(self.EV_KND) + " " + str(self.NAIYO)

    EV_DATE = models.DateField(default=None)
    EV_KND  = models.ForeignKey(MT_EVENT_KND,on_delete=models.PROTECT)
    RIYOSYA = models.ForeignKey(DT_RIYOSYA,on_delete=models.PROTECT,null=True,blank=True)
    EV_TIME = models.TimeField(null=True,blank=True)
    HT_KBN  = models.ForeignKey(MT_HC_KND,on_delete=models.PROTECT,null=True,blank=True,)
    EV_GO   = models.ForeignKey(MT_GAIBU,on_delete=models.PROTECT,null=True,blank=True,)
    D_STAFF = models.ForeignKey(MT_STAFF,on_delete=models.PROTECT,null=True,blank=True,related_name="D_STAFF")
    T_STAFF = models.ForeignKey(MT_STAFF,on_delete=models.PROTECT,null=True,blank=True,related_name="T_STAFF")
    NAIYO = models.CharField(max_length=200,null=True,blank=True)


class Shift(models.Model):
    def __str__(self):
        return str(self.shift_date)
    shift_date = models.DateField(default=None, unique=True)
    hayaban    = models.ForeignKey(MT_STAFF,related_name='hayaban',   on_delete=models.CASCADE, null=True,blank=True,)
    hayaban_e  = models.ForeignKey(MT_STAFF,related_name='hayaban_e', on_delete=models.CASCADE, null=True,blank=True,)
    nikkin     = models.ForeignKey(MT_STAFF,related_name='nikkin',    on_delete=models.CASCADE, null=True,blank=True,)
    nikkin1    = models.ForeignKey(MT_STAFF,related_name='nikkin1',   on_delete=models.CASCADE, null=True,blank=True,)
    nikkin2    = models.ForeignKey(MT_STAFF,related_name='nikkin2',   on_delete=models.CASCADE, null=True,blank=True,)
    nikkin3    = models.ForeignKey(MT_STAFF,related_name='nikkin3',   on_delete=models.CASCADE, null=True,blank=True,)
    nikkin_e   = models.ForeignKey(MT_STAFF,related_name='nikkin_e',  on_delete=models.CASCADE, null=True,blank=True,)
    nikkin_e1  = models.ForeignKey(MT_STAFF,related_name='nikkin_e1', on_delete=models.CASCADE, null=True,blank=True,)
    nikkin_e2  = models.ForeignKey(MT_STAFF,related_name='nikkin_e2', on_delete=models.CASCADE, null=True,blank=True,)
    nikkin_e3  = models.ForeignKey(MT_STAFF,related_name='nikkin_e3', on_delete=models.CASCADE, null=True,blank=True,)
    osoban     = models.ForeignKey(MT_STAFF,related_name='osoban',    on_delete=models.CASCADE, null=True,blank=True,)
    osoban_e   = models.ForeignKey(MT_STAFF,related_name='osoban_e',  on_delete=models.CASCADE, null=True,blank=True,)
    yakin      = models.ForeignKey(MT_STAFF,related_name='yakin',     on_delete=models.CASCADE, null=True,blank=True,)
    ake        = models.ForeignKey(MT_STAFF,related_name='ake',       on_delete=models.CASCADE, null=True,blank=True,)
    kango1     = models.ForeignKey(MT_STAFF,related_name='kango1',    on_delete=models.CASCADE, null=True,blank=True,)
    kango2     = models.ForeignKey(MT_STAFF,related_name='kango2',    on_delete=models.CASCADE, null=True,blank=True,)
    soudanin   = models.ForeignKey(MT_STAFF,related_name='soudanin',  on_delete=models.CASCADE, null=True,blank=True,)
    seisou     = models.ForeignKey(MT_STAFF,related_name='seisou',    on_delete=models.CASCADE, null=True,blank=True,)
    memo       = models.CharField(max_length=1000, null=True,blank=True,)
