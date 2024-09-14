from django.contrib import admin
from .models import Message, Survey, Vote,Lesson,Task

admin.site.register([Message,Survey,Vote,Lesson,Task])
