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


class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    file = models.FileField(upload_to='files/')
    
    def __str__(self):
        return self.name
    
    
class Module(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Lessons(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_teacher')
    video_link = models.CharField(max_length=150, blank=True, null=True)
    file = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='lesson_students', blank=True, null=True)
    students = models.ManyToManyField(User)
    lesson_date = models.DateTimeField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')

    
    def __str__(self):
        return f'{self.name} - {self.lesson_date}'

class Assessment(models.Model):
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='assessments')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_assessments')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_assessments')
    score = models.IntegerField(default=0)  # 0-100 oralig'ida baho
    comment = models.TextField(blank=True, null=True)  # Ixtiyoriy izoh
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['lesson', 'student', 'teacher'], 
                name='unique_lesson_student_assessment'
            )
        ]
        
    def __str__(self):
        return f'{self.student.username} - {self.lesson.name} - {self.score}'

class Test(models.Model):
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    excel_file = models.FileField(upload_to='test_files/')
    max_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    
    def __str__(self):
        return f"{self.title} - {self.lesson.name}"

class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results')
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    answers = models.JSONField()  # Studentning javoblarini saqlash uchun
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['test', 'student'], 
                name='unique_test_student'
            )
        ]
    
    def __str__(self):
        return f"{self.student.username} - {self.test.title} - {self.score}"


    