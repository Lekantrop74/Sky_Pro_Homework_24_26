from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import IsModeratorOrReadOnly
from .serializers import *


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated | IsModeratorOrReadOnly]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonCreateApiView(generics.CreateAPIView):
    permission_classes = [IsModeratorOrReadOnly]
    serializer_class = LessonSerializer


class LessonListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveApiView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateApiView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyApiView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Lesson.objects.all()


class PaymentListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payment_date', 'course_or_lesson', 'payment_method']
