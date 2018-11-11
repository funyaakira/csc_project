from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(MT_SYOKUMU)
admin.site.register(MT_STAFF)
admin.site.register(Shift)
