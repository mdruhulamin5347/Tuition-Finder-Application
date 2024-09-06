from django.contrib import admin
from .models import UserProfile, TeacherProfile

admin.site.register(UserProfile)
admin.site.register(TeacherProfile)