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
from rest_framework.decorators import api_view, authentication_classes, permission_classes 

basic_auth_param = openapi.Parameter(
    'Basic Authorization',
    openapi.IN_HEADER,
    description="Base64",
    type=openapi.TYPE_STRING
)

token_auth_param = openapi.Parameter(
    'Token Authorization',
    openapi.IN_HEADER,
    description="Token",
    type=openapi.TYPE_STRING
)


class SignIn(APIView):
    authentication_classes = [BasicAuthentication]
    @swagger_auto_schema(
        manual_parameters=[basic_auth_param],
        responses={
            '200': openapi.Response(description='User authenticated successfully'),
            '401': openapi.Response(description='Invalid credentials'),
        },
        description='User login'
    )
    def post(self, request, *args, **kwargs):
        user =request.user
        tkn, user = Token.objects.get_or_create(user=user)
        return Response({"token": tkn.key}, status=status.HTTP_200_OK)

