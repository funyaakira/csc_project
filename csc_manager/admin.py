from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(MT_SYOKUMU)
admin.site.register(MT_STAFF)
admin.site.register(MT_BASE_SCHEDULE)
admin.site.register(DT_SHIFT)
