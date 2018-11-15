from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

gender = (
    (1, '男'),
    (2, '女'),
)

ht_kbn = (
    ("発", '発'),
    ("着", '着'),
)

shift_catergory = (
    ('出', '出'),
    ('休', '休')
)

class Kyotaku(models.Model):
    name = models.CharField(max_length=200)
    fullname = models.CharField(max_length=200, default=None)
    tel = models.CharField(max_length=200)
    addr = models.CharField(max_length=200, default=None)


class CareManager(models.Model):
    kyotaku = models.ForeignKey(Kyotaku, related_name='kyotaku', on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.kyotaku.name + ' - ' + self.name


class Riyosya(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(_("氏名"), max_length=200)
    furigana = models.CharField(_("ふりがな"), max_length=200)
    sex = models.IntegerField(_("性別"), choices=gender, default=None)
    birthday = models.DateField(_("生年月日"), null=True, default=None)
    caremanager = models.ForeignKey(CareManager, verbose_name=_("ケアマネージャー"), related_name='caremanager', on_delete=models.PROTECT, default=None)
    first_day = models.DateField(_("初回入所日"), null=True, default=None)
    last_day = models.DateField(_("最終退所日"), null=True, default=None)
    taisyo_flg = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='riyosya', default=None, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='+', default=None)


class RiyosyaRenrakusaki(models.Model):
    riyosya = models.ForeignKey(Riyosya, verbose_name=_("利用者"), related_name='riyosya_renrakusaki', on_delete=models.PROTECT, default=None)
    name =  models.CharField(_("氏名"), max_length=200)
    furigana = models.CharField(_("ふりがな"), max_length=200)
    zokugara = models.CharField(_("続柄"), max_length=200)
    addr = models.CharField(_("住所"), max_length=200)
    tel = models.CharField(_("電話番号"), max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='riyosya_renrakusaki', default=None)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='+', default=None)


class RiyosyaRiyouKikan(models.Model):
    riyosya = models.ForeignKey(Riyosya, verbose_name=_("利用者"), related_name='riyosya_riyoukikan', on_delete=models.PROTECT, default=None)
    start_day = models.DateField(_("入所日"), null=True, default=None)
    last_day = models.DateField(_("退所日"), null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='riyosya_riyoukikan', default=None)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='+', default=None)


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


class Event(models.Model):
    date = models.DateField(default=None)
    knd  = models.ForeignKey(Event_knd,on_delete=models.PROTECT)
    riyosya = models.ForeignKey(Riyosya,on_delete=models.PROTECT,null=True,blank=True)
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

class Test(models.Model):
    col1 = models.CharField(max_length=200)
    col2 = models.CharField(max_length=200)
    col3 = models.CharField(max_length=200)
