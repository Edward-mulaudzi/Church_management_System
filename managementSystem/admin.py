from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(church_branch)
admin.site.register(church_member)
admin.site.register(Role)
admin.site.register(Attendance)
admin.site.register(Attendance_date)
admin.site.register(Attendance_List)
