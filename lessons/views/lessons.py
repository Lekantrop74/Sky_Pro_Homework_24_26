from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from lessons.models import Lesson
from lessons.pagination import DataPaginator
from lessons.permissions import IsModeratorOrReadOnly, IsModeratorEditOnly
from lessons.serializers import LessonSerializer


# Класс для списка уроков
class LessonListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    pagination_class = DataPaginator

    def get_queryset(self):
        user = self.request.user

        # Пользователи-модераторы или администраторы видят все уроки
        if user.is_staff or user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()

        # Обычные пользователи видят только свои уроки
        return Lesson.objects.filter(owner=user)


class LessonCreateApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsModeratorEditOnly]
    serializer_class = LessonSerializer


# Класс для просмотра урока
class LessonRetrieveApiView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


# Класс для обновления урока
class LessonUpdateApiView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated | IsModeratorOrReadOnly]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


# Класс для удаления урока
class LessonDestroyApiView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsModeratorEditOnly]
    queryset = Lesson.objects.all()
