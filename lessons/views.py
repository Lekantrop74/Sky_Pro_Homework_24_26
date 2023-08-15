from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsModeratorEditOnly, IsModeratorOrReadOnly
from .models import Course, Lesson, Payment
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer


# Класс для управления курсами
class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user

        # Пользователи-модераторы или администраторы видят все курсы
        if user.is_staff or user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()

        # Обычные пользователи видят только свои курсы
        return Course.objects.filter(owner=user)


# Класс для создания новых уроков
class LessonCreateApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsModeratorEditOnly]
    serializer_class = LessonSerializer


# Класс для списка уроков
class LessonListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user

        # Пользователи-модераторы или администраторы видят все уроки
        if user.is_staff or user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()

        # Обычные пользователи видят только свои уроки
        return Lesson.objects.filter(owner=user)


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


# Класс для списка платежей
class PaymentListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payment_date', 'course_or_lesson', 'payment_method']
