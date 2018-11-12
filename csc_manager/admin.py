from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(Syokumu)
admin.site.register(Staff)
admin.site.register(Event_knd)
admin.site.register(Shift_knd)

admin.site.register(Shift)
admin.site.register(t_Shift)
admin.site.register(Event)
admin.site.register(Riyosya)
