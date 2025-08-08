from django.contrib import admin
from .models import ThreadMessage,PrivateMessage,DiscussionThread

admin.site.register(DiscussionThread)
admin.site.register(ThreadMessage)
admin.site.register(PrivateMessage)
