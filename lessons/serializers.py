from rest_framework import serializers
from .models import *
from .validators import VideoLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.CharField(validators=[VideoLinkValidator()])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    subscribed_subscriptions = serializers.SerializerMethodField()

    lessons = LessonSerializer(many=True, read_only=True)

    def get_subscribed_subscriptions(self, obj):
        """ Show subscription of owners """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CourseSubscription.objects.filter(owner=request.user, course=obj, is_subscribed=True).exists()
        return False

    class Meta:
        model = Course
        fields = '__all__'

    @staticmethod
    def get_lessons_count(obj):
        return obj.lessons.count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscription
        fields = "__all__"
