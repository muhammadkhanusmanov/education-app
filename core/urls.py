from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from apis.views import (
   SignIn, SignUp, MessageView, SurveyView
)


schema_view = get_schema_view(
   openapi.Info(
      title="Education-app",
      default_version='v1',
      description="API Documentation",
      contact=openapi.Contact(email="mukhammdusmanov@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/', SignIn.as_view()),
    path('create/user/',SignUp.as_view()),
    path('send/message/',MessageView.as_view()),
    path('get/message/<str:pk>',MessageView.as_view()),
    path('create/survey/',SurveyView.as_view()),
    path('get/surveys/',SurveyView.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
