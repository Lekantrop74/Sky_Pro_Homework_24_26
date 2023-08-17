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
    lessons = LessonSerializer(many=True, read_only=True)

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