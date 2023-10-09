from django.contrib import admin

from chatbox.models import Chatting, GuestUser

admin.site.register(Chatting)
admin.site.register(GuestUser)
