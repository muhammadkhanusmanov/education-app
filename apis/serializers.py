from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Message, Survey, Vote,Lessons, Task,Module
)
class UserSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='last_name')
    full_name = serializers.CharField(source='first_name')
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'status']
        read_only_fields = ['id']
        


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']

class MessagesSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient']
        read_only_fields = ['id', 'created_at']

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'name', 'students', 'teacher', 'until_at', 'created_at']
        read_only_fields = ['created_at']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
        
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'
    

class LessonSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    module = ModuleSerializer

    class Meta:
        model = Lessons
        fields = ['id', 'name', 'description', 'teacher', 'video_link', 'file', 'students', 'lesson_date', 'module']
        read_only_fields = ['id']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']






