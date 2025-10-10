from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages as django_messages
from .models import TgUser
import telebot
# Create your views here.

def index(request):
    users = TgUser.objects.all().order_by('-created_at')[:200]
    return render(request, 'hello/index.html', {'users': users})