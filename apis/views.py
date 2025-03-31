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
from .serializers import (MessageSerializer,MessagesSerializer, SurveySerializer, VoteSerializer,
    LessonSerializer, UserSerializer,ModuleSerializer,AssessmentSerializer,TestResultSerializer,TestSerializer)
from .models import (Message,Survey,Vote,Lessons,Task,
    Module,Assessment,Test,TestResult)


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
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        manual_parameters=[basic_auth_param],
        responses={
            '200': openapi.Response(description='User authenticated successfully'),
            '401': openapi.Response(description='Invalid credentials'),
        },
        description='User login'
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        print(user)
        tkn, user1 = Token.objects.get_or_create(user=user)
        sr = UserSerializer(user)
        return Response({"token": tkn.key, 'user':sr.data}, status=status.HTTP_200_OK)

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
            tkn = Token.objects.create(user=new_user)
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
        
        
class VoteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Create a new vote",
        request_body=VoteSerializer,
        manual_parameters=[token_auth_param],
        responses={
            201: VoteSerializer,
            400: 'Bad Request',
            403: 'Forbidden: Authentication required'
        }
    )
    
    
    def put(self, request):
        data = request.data
        user = request.user
        data['student'] = user.ID
        serz = VoteSerializer(data=data)
        if serz.is_valid():
            serz.save()
            return Response(serz.data, status=status.HTTP_201_CREATED)
        return Response(serz.errors, status=status.HTTP_400_BAD_REQUEST) 


from django.contrib.auth.models import User, Group
from django.http import JsonResponse


class UserView(APIView):
    def get(self,request):
        teachers = User.objects.filter(last_name='Teacher')
        students = User.objects.filter(last_name='Student')

        return Response({
            'teachers': [{'id': user.id, 'username': user.username, 'email': user.email} for user in teachers],
            'students': [{'id': user.id, 'username': user.username, 'email': user.email} for user in students],
        })


class CreateModule(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Create a new module",
        request_body=ModuleSerializer,
        responses={201: ModuleSerializer, 400: 'Bad Request'}
    )
    def post(self, request):
        user = request.user
        if user.last_name != 'Admin':
            return Response({'status': False, 'message': 'Only admins can create LessonS'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        try:
            module = Module.objects.create(
                name=data['name'],
                description=data.get('description', '')
            )
            module.save()
            return Response({"status": "Module created successfully"}, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({"error": f"Missing required field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        modules = Module.objects.all()
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    

class LessonView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='Get lessons by module ID',
        manual_parameters=[
            token_auth_param,
            openapi.Parameter(
                'module_id',
                openapi.IN_PATH,
                description="Module ID",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: LessonSerializer(many=True),
            404: 'Module not found'
        }
    )
    def get(self, request, module_id=None, lesson_id=None):
        if module_id:
            try:
                module = Module.objects.get(id=module_id)
                lessons = Lessons.objects.filter(module=module)
                serializer = LessonSerializer(lessons, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Module.DoesNotExist:
                return Response(
                    {'error': 'Module not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        elif lesson_id:
            try:
                lesson = Lessons.objects.get(id=lesson_id)
                serializer = LessonSerializer(lesson)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Lessons.DoesNotExist:
                return Response(
                    {'error': 'Lesson not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        lessons = Lessons.objects.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary = 'Create a Lessons',
        manual_parameters = [token_auth_param],
        request_body=LessonSerializer,
        responses={
            201: LessonSerializer,
            400: 'Bad Request: Bad data',
            403: 'Forbidden'
        }
    )
    def post(self, request):
        user = request.user
        if user.last_name != 'Admin':
            return Response({'status': False, 'message': 'Only admins can create LessonS'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        serializer = LessonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary = 'Add extra data to the Lessons',
        manual_parameters = [token_auth_param],
        request_body=LessonSerializer,
        responses={
            200: LessonSerializer,
            400: 'Bad Request:Bad data',
            403: 'Forbidden'
        }
    )


    def put(self, request):
        user = request.user
        if user.last_name != 'Teacher':
            return Response({'status': False, 'message': 'Only teachers can update LessonS'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        id = data['id']
        lesson = Lessons.objects.get(id=id)
        serializer = LessonSerializer(lesson, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssessmentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Create or update student assessment",
        manual_parameters=[token_auth_param],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['lesson_id', 'student_id', 'score'],
            properties={
                'lesson_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'student_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'score': openapi.Schema(type=openapi.TYPE_INTEGER),
                'comment': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            201: AssessmentSerializer,
            400: 'Bad Request',
            403: 'Forbidden - Only teachers can assess students',
            404: 'Lesson or Student not found'
        }
    )
    def post(self, request):
        user = request.user
        if user.last_name != 'Teacher':
            return Response(
                {'error': 'Only teachers can assess students'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        data = request.data
        try:
            lesson = Lessons.objects.get(id=data['lesson_id'])
            student = User.objects.get(id=data['student_id'])
            
            # Tekshirish: o'qituvchi shu darsga tegishlimi
            if lesson.teacher != user:
                return Response(
                    {'error': 'You can only assess students in your lessons'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
                
            # Tekshirish: talaba shu darsga yozilganmi
            if student not in lesson.students.all():
                return Response(
                    {'error': 'This student is not enrolled in this lesson'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Bahoni tekshirish
            score = int(data['score'])
            if not (0 <= score <= 100):
                return Response(
                    {'error': 'Score must be between 0 and 100'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            assessment, created = Assessment.objects.update_or_create(
                lesson=lesson,
                student=student,
                teacher=user,
                defaults={
                    'score': score,
                    'comment': data.get('comment', '')
                }
            )
            
            serializer = AssessmentSerializer(assessment)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
            
        except Lessons.DoesNotExist:
            return Response(
                {'error': 'Lesson not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'Student not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
    @swagger_auto_schema(
        operation_summary="Get assessments",
        manual_parameters=[token_auth_param],
        responses={
            200: AssessmentSerializer(many=True),
            403: 'Forbidden'
        }
    )
    def get(self, request, lesson_id=None):
        user = request.user
        
        if lesson_id:
            try:
                lesson = Lessons.objects.get(id=lesson_id)
                if user.last_name == 'Teacher':
                    # O'qituvchi faqat o'z darslaridagi baholarni ko'ra oladi
                    if lesson.teacher != user:
                        return Response(
                            {'error': 'You can only view assessments for your lessons'}, 
                            status=status.HTTP_403_FORBIDDEN
                        )
                    assessments = Assessment.objects.filter(lesson=lesson)
                else:
                    # Talaba faqat o'zining baholarini ko'ra oladi
                    assessments = Assessment.objects.filter(lesson=lesson, student=user)
                
                serializer = AssessmentSerializer(assessments, many=True)
                return Response(serializer.data)
                
            except Lessons.DoesNotExist:
                return Response(
                    {'error': 'Lesson not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            if user.last_name == 'Teacher':
                # O'qituvchi barcha o'zi qo'ygan baholarni ko'radi
                assessments = Assessment.objects.filter(teacher=user)
            else:
                # Talaba barcha o'z baholarini ko'radi
                assessments = Assessment.objects.filter(student=user)
                
            serializer = AssessmentSerializer(assessments, many=True)
            return Response(serializer.data)


import pandas as pd
from datetime import datetime
from django.utils import timezone

class TestView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="Create a new test",
        manual_parameters=[token_auth_param],
        request_body=TestSerializer,
        responses={
            201: TestSerializer,
            400: 'Bad Request',
            403: 'Forbidden - Only teachers can create tests'
        }
    )
    def post(self, request):
        user = request.user
        if user.last_name != 'Teacher':
            return Response(
                {'error': 'Only teachers can create tests'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        data = request.data
        print(data)
        
        # Check if 'lesson' is in the request data
        lesson_id = data.get('lesson')
        if not lesson_id:
            return Response(
                {'error': 'Lesson ID is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            lesson = Lessons.objects.get(id=lesson_id)
        except Lessons.DoesNotExist:
            return Response(
                {'error': 'Lesson not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if lesson.teacher != user:
            return Response(
                {'error': 'You can only create tests for your lessons'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check for the required Excel file
        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return Response(
                {'error': 'Excel file is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Read the Excel file
        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return Response(
                {'error': f'Error reading Excel file: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create the test
        test = Test.objects.create(
            lesson=lesson,
            title=data['title'], 
            description=data.get('description', ''),
            max_score=data['max_score'],
            deadline=data['deadline']
        )

        # Save the Excel file
        test.excel_file = excel_file
        test.save()
        
        return Response({
            'id': test.id,
            'lesson': test.lesson.id,
            'title': test.title,
            'description': test.description,
            'max_score': test.max_score,
            'deadline': test.deadline,
            'excel_file': test.excel_file.url if test.excel_file else None
        }, status=status.HTTP_201_CREATED)
        
        
    @swagger_auto_schema(
        operation_summary="Submit test answers",
        manual_parameters=[token_auth_param],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['test_id', 'answers'],
            properties={
                'test_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'answers': openapi.Schema(type=openapi.TYPE_OBJECT),
            },
        ),
        responses={
            201: TestResultSerializer,
            400: 'Bad Request',
            403: 'Forbidden'
        }
    )
    def put(self, request):
        user = request.user
        if user.last_name != 'Student':
            return Response(
                {'error': 'Only students can submit tests'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        data = request.data
        try:
            test = Test.objects.get(id=data['test_id'])
            
            # Tekshirish: test muddati o'tmaganmi
            if timezone.now() > test.deadline:
                return Response(
                    {'error': 'Test submission deadline has passed'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Tekshirish: student shu darsga yozilganmi
            if user not in test.lesson.students.all():
                return Response(
                    {'error': 'You are not enrolled in this lesson'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
                
            # Excel fayldan savollarni va to'g'ri javoblarni o'qish
            df = pd.read_excel(test.excel_file.path)
            questions_data = {}
            i = 0
            for _, row in df.iterrows():
                questions_data[str(i)] = {
                    'correct_v': row['correct_v'],
                    'options': {
                        'v1': row['v1'],
                        'v2': row['v2'],
                        'v3': row['v3'],
                        'v4': row['v4']
                    }
                }
            i=+1
            # Javoblarni tekshirish
            student_answers = data['answers']
            correct_count = 0
            
            for q_id, selected_option in student_answers.items():
                if q_id not in questions_data:
                    return Response(
                        {'error': f'Invalid question ID: {q_id}'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if selected_option not in ['v1', 'v2', 'v3', 'v4']:
                    return Response(
                        {'error': f'Invalid option for question {q_id}: {selected_option}'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if questions_data[q_id]['correct_v'] == selected_option:
                    correct_count += 1
            
            # Ball hisoblash
            total_questions = len(questions_data)
            if total_questions == 0:
                return Response(
                    {'error': 'Test has no questions'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            score = int((correct_count / total_questions) * test.max_score)
            
            # Natijani saqlash
            result, created = TestResult.objects.update_or_create(
                test=test,
                student=user,
                defaults={
                    'score': score,
                    'answers': student_answers
                }
            )
            
            serializer = TestResultSerializer(result)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
            
        except Test.DoesNotExist:
            return Response(
                {'error': 'Test not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @swagger_auto_schema(
        
        operation_summary="Get tests",
        manual_parameters=[token_auth_param],
        responses={
            200: TestSerializer(many=True),
            403: 'Forbidden'
        }
    )
    def get(self, request, lesson_id=None):
        user = request.user
        
        if lesson_id:
            try:
                lesson = Lessons.objects.get(id=lesson_id)
                if user.last_name == 'Teacher':
                    if lesson.teacher != user:
                        return Response(
                            {'error': 'You can only view tests for your lessons'}, 
                            status=status.HTTP_403_FORBIDDEN
                        )
                    tests = Test.objects.filter(lesson=lesson)
                else:
                    if user not in lesson.students.all():
                        return Response(
                            {'error': 'You are not enrolled in this lesson'}, 
                            status=status.HTTP_403_FORBIDDEN
                        )
                    # Studentlar faqat muddati o'tmagan testlarni ko'rishi mumkin
                    tests = Test.objects.filter(
                        lesson=lesson,
                        deadline__gt=timezone.now()
                    )
                
                serializer = TestSerializer(tests, many=True)
                return Response(serializer.data)
                
            except Lessons.DoesNotExist:
                return Response(
                    {'error': 'Lesson not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            if user.last_name == 'Teacher':
                tests = Test.objects.filter(lesson__teacher=user)
            else:
                tests = Test.objects.filter(
                    lesson__students=user,
                    deadline__gt=timezone.now()
                )
                
            serializer = TestSerializer(tests, many=True)
            return Response(serializer.data)