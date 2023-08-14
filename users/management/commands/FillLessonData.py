import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from lessons.models import *


class Command(BaseCommand):
    help = 'Fill database with dummy data'

    def handle(self, *args, **options):
        User = get_user_model()
        users = User.objects.all()

        for index in range(3):
            course_defaults = {
                'preview': None,
                'description': f'Описание курса {index + 1}'
            }
            course, created = Course.objects.update_or_create(
                title=f'Курс {index + 1}',
                defaults=course_defaults
            )

            for lesson_index in range(3):
                lesson_defaults = {
                    'description': f'Описание урока {lesson_index + 1} курса {course.title}',
                    'preview': None,
                    'video_link': 'https://www.example.com',
                    'course': course
                }
                lesson, created = Lesson.objects.update_or_create(
                    title=f'Урок {lesson_index + 1} курса {course.title}',
                    defaults=lesson_defaults
                )

            for user in users:
                random_amount = round(random.uniform(50, 100), 2)
                payment_defaults = {
                    'payment_date': '2023-08-11',
                    'course_or_lesson': course,
                    'amount': random_amount,
                    'payment_method': 'cash'
                }
                payment, created = Payment.objects.update_or_create(
                    user=user,
                    course_or_lesson=course,
                    defaults=payment_defaults
                )
                payment.lessons.set(course.lessons.all())  # Attach lessons for this course

        self.stdout.write(self.style.SUCCESS('Данные по курсам, урокам и оплатам этих уроков созданы'))
