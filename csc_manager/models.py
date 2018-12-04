from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings

gender = (
    (1, '男'),
    (2, '女'),
)

ht_kbn = (
    ('発', '発'),
    ('着', '着'),
)

shift_catergory = (
    ('出', '出'),
    ('休', '休')
)

youkaigodo = (
    (1, '要支援1'),
    (2, '要支援2'),
    (3, '要介護1'),
    (4, '要介護2'),
    (5, '要介護3'),
    (6, '要介護4'),
    (7, '要介護5'),
)

start_kbn = (
    (0, '不明'),
    (1, '朝食から'),
    (2, '朝おやつから'),
    (3, '昼食から'),
    (4, '昼おやつから'),
    (5, '夕食から'),
)

last_kbn = (
    (0, '不明'),
    (1, '朝食まで'),
    (2, '朝おやつまで'),
    (3, '昼食まで'),
    (4, '昼おやつまで'),
    (5, '夕食まで'),
)

riyosya_status = (
    (0, '入所中'),
    (1, '退所'),
    (2, '入所予定'),
)

day_night = (
    (settings._NIKKIN, '日勤帯'),
    (settings._YAKIN, '夜勤帯'),
)

class Kyotaku(models.Model):
    name = models.CharField(max_length=200)
    fullname = models.CharField(max_length=200, default=None)
    tel = models.CharField(max_length=200)
    addr = models.CharField(max_length=200, default=None)


class CareManager(models.Model):
    kyotaku = models.ForeignKey(Kyotaku, related_name='kyotaku', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.kyotaku.name + ' - ' + self.name


class Riyosya(models.Model):
    name = models.CharField(_("氏名"), max_length=200)
    furigana = models.CharField(_("ふりがな"), max_length=200)
    sex = models.IntegerField(_("性別"), choices=gender, default=None)
    birthday = models.DateField(_("生年月日"), null=True, default=None)
    addr = models.CharField(_("住所"), max_length=200, default=None, blank=True, null=True)
    tel = models.CharField(_("電話番号"), max_length=200, default=None, blank=True, null=True)
    youkaigodo = models.IntegerField(_("要介護度"), choices=youkaigodo, default=None)
    caremanager = models.ForeignKey(CareManager, verbose_name=_("担当ケアマネージャー"), related_name='caremanager', on_delete=models.PROTECT, default=None)
    first_day = models.DateField(_("利用開始日"), null=True, default=None)
    last_day = models.DateField(_("最終退所日"), null=True, default=None, blank=True)
    status = models.IntegerField(_("入所ステータス"), choices=riyosya_status, default=0)
    memo = models.TextField(max_length=4000, help_text='The max length of the text is 4000.', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='riyosya', default=None, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='+', default=None)

    def __str__(self):
        return self.name

    def get_riyoukikan_latest_id(self):
        return RiyosyaRiyouKikan.objects.filter(riyosya=self).latest('id').id


class RiyosyaRenrakusaki(models.Model):
    riyosya = models.ForeignKey(Riyosya, verbose_name=_("利用者"), related_name='renrakusakis', on_delete=models.CASCADE, default=None)
    name =  models.CharField(_("氏名"), max_length=200)
    furigana = models.CharField(_("ふりがな"), max_length=200, null=True)
    zokugara = models.CharField(_("続柄"), max_length=200)
    addr = models.CharField(_("住所"), max_length=200, null=True)
    tel = models.CharField(_("電話番号"), max_length=200)
    tel2 = models.CharField(_("電話番号"), max_length=200, default=None, null=True)
    primary_flg = models.BooleanField(default=False)
    doukyo_flg = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='riyosya_renrakusaki', default=None, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='+', default=None)


class RiyosyaRiyouKikan(models.Model):
    riyosya = models.ForeignKey(Riyosya, verbose_name=_("利用者"), related_name='riyoukikans', on_delete=models.CASCADE, default=None)
    start_day = models.DateField(_("入所日"), default=None)
    start_time = models.TimeField(_("入所時間"), null=True, default=None)
    start_kbn = models.IntegerField(_("入所時間区分"), choices=start_kbn, default=0)
    last_day = models.DateField(_("退所日"), null=True, default=None)
    last_time = models.TimeField(_("退所時間"), null=True, default=None)
    last_kbn = models.IntegerField(_("退所時間区分"), choices=last_kbn, null=True, default=None)
    memo = models.TextField(max_length=4000, help_text='The max length of the text is 4000.', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='riyosya_riyoukikan', default=None)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='+', default=None)


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


class Gaibu(models.Model):
    def __str__(self):
        return self.GB_NAME
    name = models.CharField(max_length=200)


class Syokumu(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200, null=True)


class Staff(models.Model):
    def __str__(self):
        return self.name
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None, related_name='staff')
    name = models.CharField(max_length=200, null=True)
    short_name = models.CharField(max_length=200, null=True, default=None, blank=True)
    syokumu = models.ForeignKey(Syokumu, on_delete=models.CASCADE, default=None, null=True)
    fixed_shift = models.ForeignKey(Shift_knd, on_delete=models.CASCADE, null=True, default=None, blank=True)
    tel1 = models.CharField(max_length=200, null=True, default=None, blank=True)
    tel2 = models.CharField(max_length=200, null=True, default=None, blank=True)
    del_flg = models.BooleanField(default=False)


class Event_knd(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200, default=None)
    css_class = models.CharField(max_length=200, default=None)
    def __str__(self):
        return self.name


class Event(models.Model):
    date = models.DateField(_('日付'), default=None)
    knd  = models.ForeignKey(Event_knd, verbose_name=_('イベント種類'), on_delete=models.PROTECT)
    riyosya = models.ForeignKey(Riyosya, verbose_name=_('対象利用者'), on_delete=models.PROTECT, null=True, blank=True)
    time = models.TimeField(verbose_name=_('時間'), null=True, blank=True)
    ht_kbn  = models.CharField(_('発着'), max_length=1, null=True, blank=True, choices=ht_kbn, default=None)
    go_place = models.ForeignKey(Gaibu, verbose_name=_('行き先'), on_delete=models.PROTECT, null=True, blank=True,)
    d_staff = models.ForeignKey(Staff, verbose_name=_('運転手'), on_delete=models.PROTECT, null=True, blank=True, related_name="d_staff")
    t_staff = models.ForeignKey(Staff, verbose_name=_('付き添い'), on_delete=models.PROTECT, null=True, blank=True, related_name="t_staff")
    naiyo = models.CharField(_('イベント内容'), max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.date.strftime("%Y/%m/%d")) + " " + str(self.knd) + " " + str(self.naiyo)


class Shift(models.Model):
    date = models.DateField(default=None)
    shift_knd = models.ForeignKey(Shift_knd, related_name='shift_knd', on_delete=models.PROTECT)
    staff = models.ForeignKey(Staff, related_name='staff', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.date.strftime("%Y/%m/%d"))


class Renraku(models.Model):
    date = models.DateField(default=None)
    staff = models.ForeignKey(Staff, related_name='renrakus', on_delete=models.PROTECT)
    memo = models.TextField(max_length=4000, help_text='The max length of the text is 4000.', null=True)


class Renraku_kojin(models.Model):
    date = models.DateField(default=None)
    staff = models.ForeignKey(Staff, related_name='renraku_kojins', on_delete=models.PROTECT)
    riyosya = models.ForeignKey(Riyosya, verbose_name=_("利用者"), related_name='renraku_kojins', on_delete=models.CASCADE, default=None)
    memo = models.TextField(max_length=4000, help_text='The max length of the text is 4000.')


class Kiroku(models.Model):
    exec_date = models.DateField(default=None, null=True)
    date = models.DateField(_("日付"), default=None, null=True)
    time = models.TimeField(_("時間"), default=None, null=True, blank=True, help_text='全体の場合は空白にしてください。<br>入力した時間に応じて日付は自動で設定されます。') # nullの場合は全日
    disp_time = models.TimeField(_("並び用時間"), default=None, null=True, blank=True)
    day_night = models.IntegerField(_("日勤夜勤区分"), choices=last_kbn, null=True, default=None)
    riyosya = models.ForeignKey(Riyosya, verbose_name=_("利用者"), related_name='kirokus', on_delete=models.CASCADE, default=None)
    memo = models.TextField(_("内容"), max_length=4000, help_text='The max length of the text is 4000.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='kirokus', default=None)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='+', default=None)


class Test(models.Model):
    name = models.CharField(max_length=200)
    sex = models.IntegerField(_("性別"), choices=gender, default=None)
    birthday = models.DateField(default=None)
