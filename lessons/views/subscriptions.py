from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from lessons.models import CourseSubscription
from lessons.pagination import DataPaginator
from lessons.permissions import IsModeratorEditOnly
from lessons.serializers import SubscriptionSerializer


class SubscriptionListView(generics.ListAPIView):
    """ All subscriptions """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DataPaginator

    def get_queryset(self):
        user = self.request.user

        # Пользователи-модераторы или администраторы видят все уроки
        if user.is_staff or user.groups.filter(name='Модераторы').exists():
            return CourseSubscription.objects.all()

        # Обычные пользователи видят только свои уроки
        return CourseSubscription.objects.filter(owner=user)


class SubscriptionCreateView(generics.CreateAPIView):
    """ Create subscription with owner information"""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsModeratorEditOnly]


class SubscriptionUpdateView(generics.UpdateAPIView):
    """ Update information in subscription """
    queryset = CourseSubscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionDeleteView(generics.DestroyAPIView):
    """ Delete subscription """
    queryset = CourseSubscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsModeratorEditOnly]
