from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import Student, User, Advisor, Planner, Course, Major, Minor, Semester, Subject
class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'role', 'registered')
    list_filter = ('role', 'registered')
    fieldsets = DefaultUserAdmin.fieldsets + (
        (None, {'fields': ('role', 'registered')}),
    )
# Register your models here.
admin.site.register(Student)
admin.site.register(User, UserAdmin)
admin.site.register(Advisor)
admin.site.register(Planner)
admin.site.register(Course)
admin.site.register(Major)
admin.site.register(Minor)
admin.site.register(Subject)
admin.site.register(Semester)