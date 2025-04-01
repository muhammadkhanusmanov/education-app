from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from apis.views import (
    SignIn, SignUp, MessageView, SurveyView, VoteView, 
    UserView, CreateModule, LessonView, AssessmentView, TestView
)



schema_view = get_schema_view(
    openapi.Info(
        title="Learning Management System API",
        default_version='v1',
        description="API documentation for LMS",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Swagger documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Authentication
    path('signin/', SignIn.as_view(), name='signin'),
    path('signup/', SignUp.as_view(), name='signup'),
    
    # Messages
    path('messages/', MessageView.as_view(), name='send-message'),
    path('messages/<str:pk>/', MessageView.as_view(), name='get-message'),
    
    # Surveys
    path('surveys/', SurveyView.as_view(), name='surveys'),
    
    # Votes
    path('votes/', VoteView.as_view(), name='votes'),
    
    # Users
    path('users/', UserView.as_view(), name='users'),
    
    # Modules
    path('modules/', CreateModule.as_view(), name='modules'),
    
    # Lessons
    path('lessons/', LessonView.as_view(), name='lessons'),
    path('lessons/module/<int:module_id>/', LessonView.as_view(), name='module-lessons'),
    path('lessons/<int:lesson_id>/', LessonView.as_view(), name='lesson-detail'),
    
    # Assessments
    path('assessments/', AssessmentView.as_view(), name='assessments'),
    path('assessments/lesson/<int:lesson_id>/', AssessmentView.as_view(), name='lesson-assessments'),
    
    # Tests
    path('tests/', TestView.as_view(), name='tests'),
    path('tests/lesson/<int:lesson_id>/', TestView.as_view(), name='lesson-tests'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)