from django.contrib import admin
from .models import TgUser, Message
# Register your models here.

@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id','username','first_name','created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user','text','created_at')