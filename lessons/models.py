from django.conf import settings
from django.db import models

from users.models import User


class Course(models.Model):
    objects = None
    title = models.CharField(max_length=200, unique=True, verbose_name='Заголовок')
    preview = models.ImageField(upload_to='previews/', verbose_name='Превью', blank=True, null=True)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Владелец')

    def __str__(self):
        return self.title


class Lesson(models.Model):
    objects = None

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='lesson_previews/', verbose_name='Превью', null=True, blank=True)
    video_link = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс', related_name='lessons',
                               default=None)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Владелец')

    def __str__(self):
        return self.title


class Payment(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(verbose_name='Дата оплаты')
    course_or_lesson = models.ForeignKey('Course',
                                         on_delete=models.CASCADE)  # Здесь предположим, что у вас есть модель Course
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сума оплаты')
    payment_method_choices = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]
    payment_method = models.CharField(max_length=10, choices=payment_method_choices, verbose_name='Метод оплаты')
    lessons = models.ManyToManyField(Lesson, related_name='payments', blank=True)


class CourseSubscription(models.Model):
    objects = None
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь подписки',
                              related_name='User_subscription', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='course')
    is_subscribed = models.BooleanField(default=False, verbose_name='Статус подписки')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('owner', 'course')
