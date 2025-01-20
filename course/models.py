from django.db import models
from account.models import Person


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    
class MyCourses(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('person', 'course')  # Ensure a person can enroll in a course only once

    def __str__(self):
        return f'{self.person.user.email} enrolled in {self.course.title}'
    

class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    

class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    


class LessonVideo(models.Model):
    lesson = models.ForeignKey(to='Lesson', on_delete=models.CASCADE)
    video = models.FileField(upload_to='course/videos')
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)



