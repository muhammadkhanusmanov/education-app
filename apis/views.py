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

class SignUp(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[token_auth_param],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password', 'full_name', 'status'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'full_name': openapi.Schema(type=openapi.TYPE_STRING),
                'status': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            '200': openapi.Response(
                description='User created successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            '400': openapi.Response(description='Bad request'),
            '401': openapi.Response(description='Authentication credentials were not provided'),
            '403': openapi.Response(description='User is not an Admin'),
        },
        operation_description='Create a new user (Admin only)'
    )
    def post(self, request):
        user = request.user
        data = request.data
        
        if user.last_name != 'Admin':
            return Response({'error': 'Only Admin users can create new accounts'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            username = data['username']
            password = data['password']
            full_name = data['full_name']
            usr_sts = data['status']
            new_user = User.objects.create(
                username=username,
                password=make_password(password),
                first_name=full_name,
                last_name=usr_sts
            )
            new_user.save()
            tkn = Token.objects.get(user=new_user)
            return Response({'token':tkn.key},status=status.HTTP_200_OK)
        except:
            return Response({'error':'bad request'},status=status.HTTP_400_BAD_REQUEST)
        
