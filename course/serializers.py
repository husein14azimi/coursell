# account.serializers

from rest_framework import serializers
from .models import Course, MyCourses, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        source='category', 
        write_only=True,  # For deserialization (request)
        allow_null=True   # category is optional
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'price', 'category', 'category_id',]


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