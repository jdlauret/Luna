from django.contrib import admin
from .models import Auth_Employee, Meeting_Time, Project_Name, Project_Time, Training_Time

admin.site.register(Auth_Employee)
admin.site.register(Meeting_Time)
admin.site.register(Project_Time)
admin.site.register(Project_Name)
admin.site.register(Training_Time)