# account.urls

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import CourseViewSet, ChapterViewSet, LessonViewSet, LessonVideoViewSet

router = DefaultRouter()
router.register(r'', CourseViewSet, basename='course')

courses_router = routers.NestedDefaultRouter(router, r'', lookup='course')
courses_router.register(r'chapters', ChapterViewSet, basename='course-chapters')

chapters_router = routers.NestedDefaultRouter(courses_router, r'chapters', lookup='chapter')
chapters_router.register(r'lessons', LessonViewSet, basename='chapter-lessons')

lessons_router = routers.NestedDefaultRouter(chapters_router, r'lessons', lookup='lesson')
lessons_router.register(r'videos', LessonVideoViewSet, basename='lesson-videos')



urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(courses_router.urls)),
    path(r'', include(chapters_router.urls)),
    path(r'', include(lessons_router.urls)),
]