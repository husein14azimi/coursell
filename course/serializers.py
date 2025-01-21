# account.serializers

from rest_framework import serializers
from .models import Course, MyCourses, Category
from jalali.serializers import JalaliDateTimeField


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
    uploaded_at = JalaliDateTimeField()
    class Meta:
        model = LessonVideo
        fields = ['id', 'lesson', 'title', 'video', 'description', 'uploaded_at']
        read_only_fields = ['uploaded_at']


from .models import Transaction
class TransactionSerializer(serializers.ModelSerializer):
    created_at = JalaliDateTimeField()
    class Meta:
        model = Transaction
        fields = ['id', 'person', 'course', 'amount', 'created_at']
        read_only_fields = ['created_at']


from .models import DiscountCode, UserDiscountCode
class DiscountCodeSerializer(serializers.ModelSerializer):
    valid_from = JalaliDateTimeField()
    valid_until = JalaliDateTimeField()
    created_at = JalaliDateTimeField()
    updated_at = JalaliDateTimeField()
    class Meta:
        model = DiscountCode
        fields = ['id', 'code', 'discount_percentage', 'maximum_discount_amount', 'is_active', 'valid_from', 'valid_until', 'created_at', 'updated_at',]
        read_only_fields = ['id', 'created_at', 'updated_at',]
class UserDiscountCodeSerializer(serializers.ModelSerializer):
    created_at = JalaliDateTimeField()
    class Meta:
        model = UserDiscountCode
        fields = ['id', 'person', 'discount_code', 'transaction', 'created_at',]
        read_only_fields = ['id', 'person', 'discount_code', 'transaction', 'created_at',]