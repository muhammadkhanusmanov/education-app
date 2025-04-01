# Learning Management System API Documentation

A Django REST API for managing an educational platform with features for students, teachers, and administrators.

## Table of Contents
- [Authentication](#authentication)
- [Users](#users)
- [Modules](#modules)
- [Lessons](#lessons)
- [Messages](#messages)
- [Surveys](#surveys)
- [Assessments](#assessments)
- [Tests](#tests)

## Setup




## API Documentation

API documentation is available at:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## Authentication

### Sign In
- **Endpoint**: `POST /api/signin/`
- **Authentication**: Basic Authentication
- **Description**: Authenticate user and get token
- **Request Headers**:
  - `Authorization: Basic base64(username:password)`
- **Response**:
  ```json
  {
    "token": "your-auth-token",
    "user": {
      "id": 1,
      "username": "user1",
      "full_name": "John Doe",
      "status": "Student"
    }
  }
  ```

### Sign Up
- **Endpoint**: `POST /api/signup/`
- **Authentication**: Token Authentication (Admin only)
- **Description**: Create new user account
- **Request Body**:
  ```json
  {
    "username": "newuser",
    "password": "userpass",
    "full_name": "New User",
    "status": "Student"
  }
  ```

## Users

### List Users
- **Endpoint**: `GET /api/users/`
- **Description**: Get list of teachers and students
- **Response**: Lists of teachers and students with their details

## Modules

### Create Module
- **Endpoint**: `POST /api/modules/`
- **Authentication**: Token (Admin only)
- **Request Body**:
  ```json
  {
    "name": "Module Name",
    "description": "Module Description"
  }
  ```

### List Modules
- **Endpoint**: `GET /api/modules/`
- **Authentication**: Token
- **Description**: Get all modules

## Lessons

### Create Lesson
- **Endpoint**: `POST /api/lessons/`
- **Authentication**: Token (Admin only)
- **Request Body**:
  ```json
  {
    "name": "Lesson Name",
    "description": "Lesson Description",
    "teacher": 1,
    "video_link": "https://example.com/video",
    "file": 1,
    "students": [1, 2, 3],
    "lesson_date": "2024-03-20T10:00:00Z",
    "module": 1
  }
  ```

### Get Lessons
- **Endpoint**: `GET /api/lessons/`
- **Endpoint**: `GET /api/lessons/module/{module_id}/`
- **Endpoint**: `GET /api/lessons/{lesson_id}/`
- **Authentication**: Token

### Update Lesson
- **Endpoint**: `PUT /api/lessons/`
- **Authentication**: Token (Teacher only)

## Messages

### Send Message
- **Endpoint**: `POST /api/messages/`
- **Authentication**: Token
- **Request Body**:
  ```json
  {
    "recipient_id": 1,
    "content": "Message content"
  }
  ```

### Get Messages
- **Endpoint**: `GET /api/messages/msg/`
- **Endpoint**: `GET /api/messages/{message_id}/`
- **Authentication**: Token

## Surveys

### Create Survey
- **Endpoint**: `PUT /api/surveys/`
- **Authentication**: Token (Admin only)
- **Request Body**:
  ```json
  {
    "name": "Survey Name",
    "students": [1, 2, 3],
    "teacher": 1,
    "until_at": "2024-03-30T23:59:59Z"
  }
  ```

### Get Surveys
- **Endpoint**: `GET /api/surveys/`
- **Authentication**: Token

## Assessments

### Create Assessment
- **Endpoint**: `POST /api/assessments/`
- **Authentication**: Token (Teacher only)
- **Request Body**:
  ```json
  {
    "lesson_id": 1,
    "student_id": 1,
    "score": 85,
    "comment": "Good work"
  }
  ```

### Get Assessments
- **Endpoint**: `GET /api/assessments/`
- **Endpoint**: `GET /api/assessments/lesson/{lesson_id}/`
- **Authentication**: Token

## Tests

### Create Test
- **Endpoint**: `POST /api/tests/`
- **Authentication**: Token (Teacher only)
- **Request Body**: Multipart Form Data
  ```json
  {
    "lesson": 1,
    "title": "Test Title",
    "description": "Test Description",
    "excel_file": [file],
    "max_score": 100,
    "deadline": "2024-03-30T23:59:59Z"
  }
  ```

### Submit Test
- **Endpoint**: `PUT /api/tests/`
- **Authentication**: Token (Student only)
- **Request Body**:
  ```json
  {
    "test_id": 1,
    "answers": {
      "0": "v1",
      "1": "v3",
      "2": "v2"
    }
  }
  ```

### Get Tests
- **Endpoint**: `GET /api/tests/`
- **Endpoint**: `GET /api/tests/lesson/{lesson_id}/`
- **Authentication**: Token

## Models

### User Types
- Admin (last_name = "Admin")
- Teacher (last_name = "Teacher")
- Student (last_name = "Student")

### Message
- sender (User)
- recipient (User)
- content (Text)
- created_at (DateTime)

### Survey
- name (CharField)
- students (ManyToMany - User)
- teacher (ForeignKey - User)
- until_at (DateTime)
- created_at (DateTime)

### Vote
- student (ForeignKey - User)
- survey (ForeignKey - Survey)
- skill1-10 (Integer)
- choice1-5 (CharField)

### Module
- name (CharField)
- description (TextField)

### Lesson
- name (CharField)
- description (TextField)
- teacher (ForeignKey - User)
- video_link (CharField)
- file (ForeignKey - Task)
- students (ManyToMany - User)
- lesson_date (DateTime)
- module (ForeignKey - Module)

### Assessment
- lesson (ForeignKey - Lesson)
- student (ForeignKey - User)
- teacher (ForeignKey - User)
- score (Integer)
- comment (TextField)
- created_at (DateTime)

### Test
- lesson (ForeignKey - Lesson)
- title (CharField)
- description (TextField)
- excel_file (FileField)
- max_score (Integer)
- created_at (DateTime)
- deadline (DateTime)

### TestResult
- test (ForeignKey - Test)
- student (ForeignKey - User)
- score (Integer)
- submitted_at (DateTime)
- answers (JSONField)

## Authentication and Permissions

- Basic Authentication: Used for initial login
- Token Authentication: Used for all other endpoints
- Admin permissions: Required for user creation and certain administrative tasks
- Teacher permissions: Required for assessment creation and test management
- Student permissions: Limited to viewing and submitting tests, viewing assessments

## File Handling

Media files are stored in the `media/` directory and are served at `/media/` URLs in development.