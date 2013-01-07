from django.contrib import admin
from models import RegisteredUsers
class RegisteredUsersAdmin(admin.ModelAdmin):
    list_display = ('name','email','city')
    list_filter = ('city','bloodgroup')
admin.site.register(RegisteredUsers,RegisteredUsersAdmin)