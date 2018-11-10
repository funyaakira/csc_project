from django.db import models

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

    EV_DATE = models.DateField()
    EV_KND  = models.ForeignKey(MT_EVENT_KND,on_delete=models.PROTECT)
    RIYOSYA = models.ForeignKey(DT_RIYOSYA,on_delete=models.PROTECT,null=True,blank=True)
    EV_TIME = models.TimeField(null=True,blank=True)
    HT_KBN  = models.ForeignKey(MT_HC_KND,on_delete=models.PROTECT,null=True,blank=True,)
    EV_GO   = models.ForeignKey(MT_GAIBU,on_delete=models.PROTECT,null=True,blank=True,)
    D_STAFF = models.ForeignKey(MT_STAFF,on_delete=models.PROTECT,null=True,blank=True,related_name="D_STAFF")
    T_STAFF = models.ForeignKey(MT_STAFF,on_delete=models.PROTECT,null=True,blank=True,related_name="T_STAFF")
    NAIYO = models.CharField(max_length=200,null=True,blank=True)


class DT_SHIFT(models.Model):
    def __str__(self):
        return str(self.SHIFT_DATE)
    SHIFT_DATE = models.DateField(null=True,unique=True,blank=True,)
    HAYABAN    = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_HAYABAN',   on_delete=models.CASCADE, null=True,blank=True,)
    HAYABAN_E  = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_HAYABAN_E', on_delete=models.CASCADE, null=True,blank=True,)
    NIKKIN     = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_NIKKIN',    on_delete=models.CASCADE, null=True,blank=True,)
    NIKKIN1    = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_NIKKIN1',   on_delete=models.CASCADE, null=True,blank=True,)
    NIKKIN2    = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_NIKKIN2',   on_delete=models.CASCADE, null=True,blank=True,)
    NIKKIN3    = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_NIKKIN3',   on_delete=models.CASCADE, null=True,blank=True,)
    NIKKIN_E   = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_NIKKIN_E',  on_delete=models.CASCADE, null=True,blank=True,)
    NIKKIN_E1  = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_NIKKIN_E1', on_delete=models.CASCADE, null=True,blank=True,)
    NIKKIN_E2  = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_NIKKIN_E2', on_delete=models.CASCADE, null=True,blank=True,)
    NIKKIN_E3  = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_NIKKIN_E3', on_delete=models.CASCADE, null=True,blank=True,)
    OSOBAN     = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_OSOBAN',    on_delete=models.CASCADE, null=True,blank=True,)
    OSOBAN_E   = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_OSOBAN_E',  on_delete=models.CASCADE, null=True,blank=True,)
    YAKIN      = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_YAKIN',     on_delete=models.CASCADE, null=True,blank=True,)
    AKE        = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_AKE',       on_delete=models.CASCADE, null=True,blank=True,)
    KANGO1     = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_KANGO1',    on_delete=models.CASCADE, null=True,blank=True,)
    KANGO2     = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_KANGO2',    on_delete=models.CASCADE, null=True,blank=True,)
    SOUDANIN   = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_SOUDANIN',  on_delete=models.CASCADE, null=True,blank=True,)
    SEISOU     = models.ForeignKey(MT_STAFF,related_name='MT_STAFF_SEISOU',    on_delete=models.CASCADE, null=True,blank=True,)
    MEMO       = models.CharField(max_length=1000, null=True,blank=True,)
