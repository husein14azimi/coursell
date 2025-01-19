# account.serializers

from rest_framework import serializers
from .models import Course, MyCourses

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title']


class MyCoursesSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = MyCourses
        fields = ['id', 'course', 'course_title']


from .models import Chapter
class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'course', 'title',]


from .models import Lesson
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'chapter', 'title', 'description']



from .models import LessonVideo
class LessonVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonVideo
        fields = ['id', 'lesson', 'title', 'video', 'description', 'uploaded_at']
        read_only_fields = ['uploaded_at']