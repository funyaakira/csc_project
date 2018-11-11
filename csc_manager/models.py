from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

Gender = (
    ("女性", '女性'),
    ("男性", '男性'),
)

ht_kbn  = (
    ("発", '発'),
    ("着", '着'),
)

class Event_knd(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)

class MT_GAIBU(models.Model):
    def __str__(self):
        return self.GB_NAME
    GB_NAME = models.CharField(max_length=200)

class MT_SYOKUMU(models.Model):
    def __str__(self):
        return self.SYOKUMU_NAME
    SYOKUMU_NAME = models.CharField(max_length=200, null=True)

class StaffInfo(models.Model):
    def __str__(self):
        return self.name
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None)
    name = models.CharField(max_length=200, null=True)
    syokumu = models.ForeignKey(MT_SYOKUMU, on_delete=models.CASCADE, default=None)
    del_flg = models.BooleanField(default=False)

class Riyosya(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)
    furigana = models.CharField(max_length=200)
    sex = models.CharField(_("性別"), max_length=2, choices=Gender, default=None)
    birthday = models.DateField(null=True, default=None)
    taisyo_flg = models.BooleanField(default=False)


class Event(models.Model):
    def __str__(self):
        return str(self.date.strftime("%Y/%m/%d")) + " " + str(self.knd) + " " + str(self.naiyo)

    date = models.DateField(default=None)
    knd  = models.ForeignKey(Event_knd,on_delete=models.PROTECT)
    Riyosya = models.ForeignKey(Riyosya,on_delete=models.PROTECT,null=True,blank=True)
    time = models.TimeField(null=True,blank=True)
    ht_kbn  = models.CharField(_("発着"), max_length=1, blank=True, choices=ht_kbn, default=None)
    go_place = models.ForeignKey(MT_GAIBU,on_delete=models.PROTECT,null=True,blank=True,)
    d_staff = models.ForeignKey(StaffInfo,on_delete=models.PROTECT,null=True,blank=True,related_name="d_staff")
    t_staff = models.ForeignKey(StaffInfo,on_delete=models.PROTECT,null=True,blank=True,related_name="t_staff")
    naiyo = models.CharField(max_length=200,null=True,blank=True)

class Shift(models.Model):
    def __str__(self):
        return str(self.date)
    date = models.DateField(default=None, unique=True)
    hayaban    = models.ForeignKey(StaffInfo,related_name='hayaban',   on_delete=models.CASCADE, null=True,blank=True,)
    hayaban_e  = models.ForeignKey(StaffInfo,related_name='hayaban_e', on_delete=models.CASCADE, null=True,blank=True,)
    nikkin     = models.ForeignKey(StaffInfo,related_name='nikkin',    on_delete=models.CASCADE, null=True,blank=True,)
    nikkin1    = models.ForeignKey(StaffInfo,related_name='nikkin1',   on_delete=models.CASCADE, null=True,blank=True,)
    nikkin2    = models.ForeignKey(StaffInfo,related_name='nikkin2',   on_delete=models.CASCADE, null=True,blank=True,)
    nikkin3    = models.ForeignKey(StaffInfo,related_name='nikkin3',   on_delete=models.CASCADE, null=True,blank=True,)
    nikkin_e   = models.ForeignKey(StaffInfo,related_name='nikkin_e',  on_delete=models.CASCADE, null=True,blank=True,)
    nikkin_e1  = models.ForeignKey(StaffInfo,related_name='nikkin_e1', on_delete=models.CASCADE, null=True,blank=True,)
    nikkin_e2  = models.ForeignKey(StaffInfo,related_name='nikkin_e2', on_delete=models.CASCADE, null=True,blank=True,)
    nikkin_e3  = models.ForeignKey(StaffInfo,related_name='nikkin_e3', on_delete=models.CASCADE, null=True,blank=True,)
    osoban     = models.ForeignKey(StaffInfo,related_name='osoban',    on_delete=models.CASCADE, null=True,blank=True,)
    osoban_e   = models.ForeignKey(StaffInfo,related_name='osoban_e',  on_delete=models.CASCADE, null=True,blank=True,)
    yakin      = models.ForeignKey(StaffInfo,related_name='yakin',     on_delete=models.CASCADE, null=True,blank=True,)
    ake        = models.ForeignKey(StaffInfo,related_name='ake',       on_delete=models.CASCADE, null=True,blank=True,)
    kango1     = models.ForeignKey(StaffInfo,related_name='kango1',    on_delete=models.CASCADE, null=True,blank=True,)
    kango2     = models.ForeignKey(StaffInfo,related_name='kango2',    on_delete=models.CASCADE, null=True,blank=True,)
    soudanin   = models.ForeignKey(StaffInfo,related_name='soudanin',  on_delete=models.CASCADE, null=True,blank=True,)
    seisou     = models.ForeignKey(StaffInfo,related_name='seisou',    on_delete=models.CASCADE, null=True,blank=True,)
    memo       = models.CharField(max_length=1000, null=True,blank=True,)
