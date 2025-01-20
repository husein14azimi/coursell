# account.views

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from .models import Course, MyCourses
from account.models import Person
from .serializers import CourseSerializer, MyCoursesSerializer
from django.contrib.auth import get_user_model
from .permissions import UserIsEnrolledInTheCourse, UserIsTheInstructorOfTheCourse

User = get_user_model()

# course/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Category, Course
from .serializers import CategorySerializer, CourseSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]  # Only admin users can perform write operations

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        return [IsAdminUser()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        courses = Course.objects.filter(category=instance).select_related('category')
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().select_related('category')
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        person = Person.objects.get(user=user)

        if person.is_student:  # Only instructors can create courses
            return Response({"detail": "You are registered as a student. You do not have permission to create courses."}, status=403)

        # course = Course.objects.create(title=request.data['title'])
        # Use the serializer to validate the data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Create the course with the serializer (the general way, best practice - includes category)
        course = serializer.save()
        MyCourses.objects.create(person=person, course=course)  # Automatically enroll the instructor in their course
        return Response(CourseSerializer(course).data, status=201)

    def update(self, request, *args, **kwargs):
        course = self.get_object()
        person = Person.objects.get(user=request.user)

        if not person.is_student and MyCourses.objects.filter(person=person, course=course).exists():
            serializer = self.get_serializer(course, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response({"detail": "This course dosn't belong to you. You do not have permission to update this course."}, status=403)


    @action(
            detail=True,
            methods=['post'],
            # permission_classes=[IsAuthenticated]
            )
    def enroll(self, request, pk=None):
        course = self.get_object()
        person = Person.objects.get(user=request.user)

        if person.is_student:
            MyCourses.objects.get_or_create(person=person, course=course)
            return Response({"detail": "Successfully enrolled in the course."}, status=200)
        return Response({"detail": "Only students can enroll in courses."}, status=403)
    

    @action(
            detail=False,
            methods=['get'],
            # permission_classes=[IsAuthenticated]
            )
    def my_courses(self, request):
        person = Person.objects.get(user=request.user)
        my_courses = MyCourses.objects.filter(person=person)
        serializer = MyCoursesSerializer(my_courses, many=True)
        return Response(serializer.data)






from .models import Chapter
from .serializers import ChapterSerializer

class ChapterViewSet(viewsets.ModelViewSet):
    serializer_class = ChapterSerializer
    # permission_classes = [IsAuthenticated, IsEnrolledInCourse]

    def get_queryset(self):
        course_id = self.kwargs.get('course_pk')
        return Chapter.objects.filter(course_id=course_id)
        
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return [UserIsEnrolledInTheCourse()]
        return [UserIsTheInstructorOfTheCourse()]


from .models import Lesson
from .serializers import LessonSerializer
class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        chapter_id = self.kwargs.get('chapter_pk')
        return Lesson.objects.filter(chapter_id=chapter_id)
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return [UserIsEnrolledInTheCourse()]
        return [UserIsTheInstructorOfTheCourse()]

    def perform_create(self, serializer):
        person = Person.objects.get(user=self.request.user)
        chapter_id = self.kwargs.get('chapter_pk')
        chapter = Chapter.objects.filter(pk=chapter_id).first()

        serializer.save(chapter=chapter)
    



from .models import LessonVideo
from .serializers import LessonVideoSerializer

class LessonVideoViewSet(viewsets.ModelViewSet):
    serializer_class = LessonVideoSerializer

    def get_queryset(self):
        lesson_id = self.kwargs.get('lesson_pk')
        return LessonVideo.objects.filter(lesson_id=lesson_id)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return [UserIsEnrolledInTheCourse()]
        return [UserIsTheInstructorOfTheCourse()]

    def perform_create(self, serializer):
        lesson_id = self.kwargs.get('lesson_pk')
        lesson = Lesson.objects.get(pk=lesson_id)
        serializer.save(lesson=lesson)
