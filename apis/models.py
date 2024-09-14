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
    until_at = models.DateTimeField(default=None,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name} ({self.created_at} - {self.until_at})'
    
class Vote(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE, related_name='vote')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='vote')
    skill1 = models.IntegerField(default=0)
    skill2 = models.IntegerField(default=0)
    skill3 = models.IntegerField(default=0)
    skill4 = models.IntegerField(default=0)
    skill5 = models.IntegerField(default=0)
    skill6 = models.IntegerField(default=0)
    skill7 = models.IntegerField(default=0)
    skill8 = models.IntegerField(default=0)
    skill9 = models.IntegerField(default=0)
    skill10 = models.IntegerField(default=0)
    choice1 = models.CharField(max_length=10)
    choice2 = models.CharField(max_length=10)
    choice3 = models.CharField(max_length=10)
    choice4 = models.CharField(max_length=10)
    choice5 = models.CharField(max_length=10)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'survey'], name='unique_student_survey')
        ]

    def __str__(self) -> str:
        return f'{self.student.username} - {self.survey.name}'