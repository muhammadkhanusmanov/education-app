from django.contrib import admin
from .models import Message, Survey, Vote

admin.site.register([Message,Survey,Vote])
