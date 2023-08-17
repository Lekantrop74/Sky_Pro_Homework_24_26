from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from lessons.models import Course
from lessons.pagination import DataPaginator
from lessons.permissions import IsModeratorEditOnly
from lessons.serializers import CourseSerializer


class CourseListView(generics.ListAPIView):
    """ Вывод всех курсов """
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DataPaginator

    def get_queryset(self):
        user = self.request.user

        # Пользователи-модераторы или администраторы видят все курсы
        if user.is_staff or user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()

        # Обычные пользователи видят только свои курсы
        return Course.objects.filter(owner=user)


class CourseDetailView(generics.RetrieveAPIView):
    """ Информация о курсе """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class CourseCreateView(generics.CreateAPIView):
    """ Создание курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModeratorEditOnly]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class CourseUpdateView(generics.UpdateAPIView):
    """ Изменение информации о курсе """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModeratorEditOnly]


class CourseDeleteView(generics.DestroyAPIView):
    """ Удаление курса """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModeratorEditOnly]