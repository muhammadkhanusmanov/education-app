from django.contrib import admin
from .models import Message, Survey

admin.site.register([Message,Survey])
