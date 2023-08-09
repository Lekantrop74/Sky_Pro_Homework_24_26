from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lessons.apps import LessonsConfig
from lessons.views import *
from users.views import UserViewSet

app_name = LessonsConfig.name

# Создаем экземпляр DefaultRouter
router = DefaultRouter()

# Регистрируем ViewSet для курсов
router.register(r'courses', CourseViewSet)

# Добавляем маршруты ViewSet к общим URL-путям
urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListApiView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateApiView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonRetrieveApiView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/update/', LessonUpdateApiView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyApiView.as_view(), name='lesson-delete'),
]