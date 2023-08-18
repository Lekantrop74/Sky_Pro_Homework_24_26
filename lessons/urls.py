from django.urls import path

from lessons.apps import LessonsConfig
from lessons.views.course import *
from lessons.views.lessons import *
from lessons.views.payment import PaymentListApiView
from lessons.views.subscriptions import *

app_name = LessonsConfig.name

# Добавляем маршруты ViewSet к общим URL-путям
urlpatterns = [
    # course
    path("courses/", CourseListView.as_view(), name="show_all_courses"),
    path("course/<int:pk>/", CourseDetailView.as_view(), name="course_show"),
    path("course/create/", CourseCreateView.as_view(), name="course_create"),
    path("course/update/<int:pk>/", CourseUpdateView.as_view(), name="course_update"),
    path("course/delete/<int:pk>/", CourseDeleteView.as_view(), name="course_delete"),
    # lessons
    path('lessons/', LessonListApiView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateApiView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonRetrieveApiView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/update/', LessonUpdateApiView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyApiView.as_view(), name='lesson-delete'),
    # subscription
    path("subscription/", SubscriptionListView.as_view(), name="show_all_subscriptions"),
    path("subscription/create/", SubscriptionCreateView.as_view(), name="subscription_create"),
    path("subscription/update/<int:pk>/", SubscriptionUpdateView.as_view(), name="subscription_update"),
    path("subscription/delete/<int:pk>/", SubscriptionDeleteView.as_view(), name="subscription_delete"),



    path('payments/', PaymentListApiView.as_view(), name='payment-list'),

]