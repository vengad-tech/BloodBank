from django.contrib import admin
from models import RegisteredUsers
from models import Feedback

class RegisteredUsersAdmin(admin.ModelAdmin):
    list_display = ('name','email','city')
    list_filter = ('city','bloodgroup')
    search_fields = ['email','name']
admin.site.register(RegisteredUsers,RegisteredUsersAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name','email','mobile','value')
admin.site.register(Feedback,FeedbackAdmin)