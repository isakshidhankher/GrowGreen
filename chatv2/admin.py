from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register((Message))

# class MessageAdmin(admin.ModelAdmin):
#     pass

class ChatAdmin(admin.ModelAdmin):
    filter_horizontal = ('participants','messages')

class ContactAdmin(admin.ModelAdmin):
    filter_horizontal = ('friend',)

admin.site.register(Contact, ContactAdmin)
admin.site.register(Chat, ChatAdmin)