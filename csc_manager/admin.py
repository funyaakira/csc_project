from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(Syokumu)
admin.site.register(Staff)
admin.site.register(Event_knd)
admin.site.register(Event_knd)
admin.site.register(Event_knd)

admin.site.register(Kyotaku)
admin.site.register(CareManager)

@admin.register(Shift_knd)
class Shift_kndAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'shift_disp_order')

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('date', 'shift_knd', 'staff')
