from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi