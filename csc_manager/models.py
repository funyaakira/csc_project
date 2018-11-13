from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

gender = (
    ("女性", '女性'),
    ("男性", '男性'),
)

ht_kbn = (
    ("発", '発'),
    ("着", '着'),
)

shift_catergory = (
    ('出', '出'),
    ('休', '休')
)

class Event_knd(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)

class Shift_knd(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200, default=None)
    shift_disp_order = models.IntegerField(unique=True, default=0)
    css_class = models.CharField(max_length=200, default=None)
    desc = models.CharField(max_length=200, default=None, null=True)
    catergory = models.CharField(max_length=2, choices=shift_catergory, default=None)
    del_flg = models.BooleanField(default=False)

class MT_GAIBU(models.Model):
    def __str__(self):
        return self.GB_NAME
    GB_NAME = models.CharField(max_length=200)

class Syokumu(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200, null=True)


class Staff(models.Model):
    def __str__(self):
        return self.name
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None)
    name = models.CharField(max_length=200, null=True)
    syokumu = models.ForeignKey(Syokumu, on_delete=models.CASCADE, default=None)
    fixed_shift = models.ForeignKey(Shift_knd, on_delete=models.CASCADE, null=True, default=None)
    del_flg = models.BooleanField(default=False)

class Riyosya(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)
    furigana = models.CharField(max_length=200)
    sex = models.CharField(_("性別"), max_length=2, choices=gender, default=None)
    birthday = models.DateField(null=True, default=None)
    taisyo_flg = models.BooleanField(default=False)


class Event(models.Model):
    date = models.DateField(default=None)
    knd  = models.ForeignKey(Event_knd,on_delete=models.PROTECT)
    Riyosya = models.ForeignKey(Riyosya,on_delete=models.PROTECT,null=True,blank=True)
    time = models.TimeField(null=True,blank=True)
    ht_kbn  = models.CharField(_("発着"), max_length=1, blank=True, choices=ht_kbn, default=None)
    go_place = models.ForeignKey(MT_GAIBU,on_delete=models.PROTECT,null=True,blank=True,)
    d_staff = models.ForeignKey(Staff,on_delete=models.PROTECT,null=True,blank=True,related_name="d_staff")
    t_staff = models.ForeignKey(Staff,on_delete=models.PROTECT,null=True,blank=True,related_name="t_staff")
    naiyo = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return str(self.date.strftime("%Y/%m/%d")) + " " + str(self.knd) + " " + str(self.naiyo)


class Shift(models.Model):
    date = models.DateField(default=None)
    shift_knd = models.ForeignKey(Shift_knd, related_name='shift_knd', on_delete=models.PROTECT)
    staff = models.ForeignKey(Staff, related_name='staff', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.date.strftime("%Y/%m/%d"))
