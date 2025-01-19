# course/permissions.py

from rest_framework import permissions
from .models import MyCourses
from account.models import Person
from django.shortcuts import get_object_or_404

class UserIsEnrolledInTheCourse(permissions.BasePermission):
    """
    Custom permission to allow enrolled students to access course-related views for read-only actions.
    """

    def has_permission(self, request, view):
        # Allow access to admin users
        if request.user.is_staff:
            return True
        
        # Get the course ID from the URL
        course_id = view.kwargs.get('course_pk') or view.kwargs.get('pk')
        
        # Get the person associated with the user
        person = get_object_or_404(Person, user=request.user)

        # Check if the user has access to the course
        return MyCourses.objects.filter(person=person, course_id=course_id).exists()

class UserIsTheInstructorOfTheCourse(permissions.BasePermission):
    """
    Custom permission to allow instructors to create, update, or delete course-related views.
    """

    def has_permission(self, request, view):
        # Allow access to admin users
        if request.user.is_staff:
            return True

        course_id = view.kwargs.get('course_pk') or view.kwargs.get('pk')
        # Get the person associated with the user
        person = get_object_or_404(Person, user=request.user)

        # Allow access if the user is an instructor
        return (MyCourses.objects.filter(person=person, course_id=course_id).exists()) and not person.is_student

