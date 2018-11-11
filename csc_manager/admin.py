from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(MT_SYOKUMU)
admin.site.register(StaffInfo)
admin.site.register(Event_knd)

admin.site.register(Shift)
admin.site.register(Event)
admin.site.register(Riyosya)
