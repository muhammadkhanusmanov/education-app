from django.contrib import admin
from .models import (Message, Survey, Vote,Lessons,
Task,Module,Assessment,Test,TestResult
)

admin.site.register([Message,Survey,Vote,Lessons,Task,Module,Assessment,Test,TestResult])
