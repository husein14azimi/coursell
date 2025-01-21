from django.db import models
from account.models import Person


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.PositiveIntegerField()

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



class Transaction(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.person.user.email} paid {self.amount} for {self.course.title} on {self.created_at}'


from django.utils import timezone

class DiscountCode(models.Model):
    code = models.CharField(max_length=255, unique=True)
    discount_percentage = models.PositiveSmallIntegerField()
    maximum_discount_amount = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    def is_valid_in_time(self):
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_until

    def calculate_discounted_price(self, price):
        # discount_amount = (self.discount_percentage / 100) * price
        # the price is coming from the outside of django; therefore, make sure it's int
        discount_amount = self.discount_percentage * int(price) / 100
        discounted_price = price - discount_amount
        return max(discounted_price, price - self.maximum_discount_amount)


class UserDiscountCode(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    discount_code = models.OneToOneField(DiscountCode, on_delete=models.CASCADE)
    transaction = models.OneToOneField('Transaction', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.person.user.email} used {self.discount_code.code}'