from django.contrib import admin
from chatMe.models import *
# Register your models here.

class MessageAdmin(admin.ModelAdmin):
    model = Media
    list_display = ('content', 'sender', 'receiver')


admin.site.register(Media)
admin.site.register(Message, MessageAdmin)
admin.site.register(Group)
admin.site.register(UserProfileImage)
