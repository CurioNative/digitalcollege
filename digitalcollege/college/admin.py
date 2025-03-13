from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Department, Subject, VideoLecture, Question, Answer

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'department', 'semester')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'department', 'semester')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(VideoLecture)
admin.site.register(Question)
admin.site.register(Answer)
