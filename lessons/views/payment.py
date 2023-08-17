from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from lessons.models import Payment
from lessons.serializers import PaymentSerializer


class PaymentListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payment_date', 'course_or_lesson', 'payment_method']