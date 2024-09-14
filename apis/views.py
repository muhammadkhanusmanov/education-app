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
from django.utils import timezone
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from .serializers import MessageSerializer,MessagesSerializer, SurveySerializer, VoteSerializer
from .models import Message,Survey,Vote


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
        
class MessageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Send a message",
        manual_parameters=[token_auth_param],
        operation_description="Send a message to another user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['recipient_id', 'content'],
            properties={
                'recipient_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the recipient user"),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description="Content of the message"),
            },
        ),
        responses={
            201: openapi.Response(
                description="Message sent successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: openapi.Response(description="Bad request"),
            404: openapi.Response(description="Recipient not found"),
        }
    )
    
    def post(self, request):
        sender = request.user
        recipient_id = request.data.get('recipient_id')
        content = request.data.get('content')

        if not recipient_id or not content:
            return Response({'error': 'Recipient ID and content are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            return Response({'error': 'Recipient not found'}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            sender=sender,
            recipient=recipient,
            content=content
        )

        message.save()
        return Response({'status':'OK'}, status=status.HTTP_201_CREATED)
    
    
    def get(self, request, pk: str):
        user = request.user
        if pk == 'msg':
            msg = Message.objects.filter(recipient=user).order_by('-created_at')
            serializer = MessagesSerializer(msg, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        try:
            msg = Message.objects.get(recipient=user,id=pk)
            msg = MessageSerializer(data=msg, many=True).data
            return Response(msg,status=status.HTTP_200_OK)
        except:
            return Response({'error':'bad request'},status=status.HTTP_400_BAD_REQUEST)

class SurveyView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Create a new survey (only Admin)",
        request_body=SurveySerializer,
        manual_parameters=[token_auth_param],
        responses={
            201: SurveySerializer,
            400: 'Bad Request',
            403: 'Forbidden: Only Admins can create surveys'
        }
    )
    
    def put(self, request):
        data = request.data
        user = request.user
        if user.last_name != 'Admin':
            return Response({'status': False},status=status.HTTP_403_FORBIDDEN)
        serl = SurveySerializer(data=data)
        if serl.is_valid():
            serl.save()
            return Response(serl.data, status=status.HTTP_201_CREATED)
        return Response(serl.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="Get the surveys user can vote",
        manual_parameters=[token_auth_param],
        responses={
            200: SurveySerializer(many=True),
            403: 'Forbidden: Authentication required',
        }
    )
    
    def get(self, request):
        user = request.user
        current_time = timezone.now()
        surveys = Survey.objects.filter(until_at__gt=current_time, students__in=[user])
        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        