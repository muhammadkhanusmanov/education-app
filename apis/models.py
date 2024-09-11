from django.contrib.auth.models import User
from django.db import models

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Message from {self.sender} to {self.recipient}'
        
class Survey(models.Model):
    name = models.CharField(max_length=50)
    students = models.ManyToManyField(User, related_name='survey')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='survey_teacher')
    untill_at = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name} ({created_at} - {untill_at})'