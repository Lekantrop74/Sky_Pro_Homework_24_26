from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from .models import Course, Lesson, Payment, CourseSubscription


# self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)



class CourseTestCase(APITestCase):
    def setUp(self) -> None:
        """
        Устанавливаем начальные данные для тестов класса CourseTestCase.
        """
        self.user = User(email='user@mail.com', first_name='Пользователь')
        self.user.set_password('testpassword')
        self.user.save()

        # Создаем и сохраняем токен авторизации
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Создаем тестовый курс для использования в тестах
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание тестового курса',
            owner=self.user
        )

    # Тест на просмотр списка курсов
    def test_course_list_view(self):
        url = reverse('lessons:show_all_courses')
        response = self.client.get(url)

        # Подготавливаем ожидаемые данные для сравнения
        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [{
                'id': self.course.id,
                'lessons_count': 0,
                'subscribed_subscriptions': False,
                'lessons': [],
                'title': 'Тестовый курс',
                'preview': None,
                'description': 'Описание тестового курса',
                'owner': self.user.id
            }]
        }

        # Сравниваем ожидаемые данные с ответом сервера
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)

    # Тест на создание нового курса
    def test_create_course(self):
        course_data = {
            'title': 'Новый курс',
            'description': 'Описание нового курса',
            # Другие необходимые поля для сериализатора
        }
        response = self.client.post(reverse('lessons:course_create'), data=course_data)

        # Проверяем, что курс был успешно создан и данные совпадают
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], course_data['title'])
        self.assertEqual(response.json()['description'], course_data['description'])

    # Тест на создание курса с некорректными данными
    def test_create_course_invalid_data(self):
        invalid_course_data = {
            'title': '',  # Неправильное значение для обязательного поля
            'description': 'Описание нового курса',
        }
        response = self.client.post(reverse('lessons:course_create'), data=invalid_course_data)

        # Проверяем, что сервер вернул ошибку и не создал курс
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Тест на обновление данных курса
    def test_update_course(self):
        updated_data = {
            'title': 'Новое название курса',
            'description': 'Новое описание курса',
            # Другие поля для сериализатора
        }
        response = self.client.put(reverse('lessons:course_update', kwargs={'pk': self.course.id}), data=updated_data)

        # Проверяем, что данные были успешно обновлены
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], updated_data['title'])
        self.assertEqual(response.json()['description'], updated_data['description'])

    # Тест на удаление курса
    def test_delete_course(self):
        response = self.client.delete(reverse('lessons:course_delete', kwargs={'pk': self.course.id}))

        # Проверяем, что курс был успешно удален
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        """
        Устанавливаем начальные данные для тестов класса LessonTestCase.
        """
        self.user = User(email='user@mail.com', first_name='Пользователь')
        self.user.set_password('testpassword')
        self.user.save()

        # Создаем и сохраняем токен авторизации
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Создаем тестовый курс и урок для использования в тестах
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание тестового курса',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            description='Описание тестового урока',
            course=self.course,
            owner=self.user
        )

    # Тест на просмотр списка уроков
    def test_lesson_list_view(self):
        url = reverse('lessons:lesson-list')
        response = self.client.get(url)

        # Подготавливаем ожидаемые данные для сравнения
        expected_data = [{
            'id': self.lesson.id,
            'video_link': None,
            'title': 'Тестовый урок',
            'description': 'Описание тестового урока',
            'preview': None,
            'course': self.lesson.course.id,
            'owner': self.lesson.owner.id,
        }]

        # Сравниваем ожидаемые данные с ответом сервера
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], expected_data)

    # Тест на создание нового урока
    def test_create_lesson(self):
        lesson_data = {
            'title': 'Новый урок',
            'description': 'Описание нового урока',
            'course': self.course.id,
            'owner': self.user.id,
            'video_link': 'https://www.youtube.com/123456',
        }
        response = self.client.post(reverse('lessons:lesson-create'), data=lesson_data)

        # Проверяем, что урок был успешно создан и данные совпадают
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], lesson_data['title'])
        self.assertEqual(response.json()['description'], lesson_data['description'])

    # Тест на обновление данных урока
    def test_update_lesson(self):
        updated_data = {
            'title': 'Новое название урока',
            'description': 'Новое описание урока',
            'course': self.course.id,
            'owner': self.user.id,
            'video_link': 'https://www.youtube.com/123457',
            # Другие поля для сериализатора
        }
        response = self.client.put(reverse('lessons:lesson-update', kwargs={'pk': self.lesson.id}), data=updated_data)

        # Проверяем, что данные были успешно обновлены
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], updated_data['title'])
        self.assertEqual(response.json()['description'], updated_data['description'])

    # Тест на удаление урока
    def test_delete_lesson(self):
        response = self.client.delete(reverse('lessons:lesson-delete', kwargs={'pk': self.lesson.id}))

        # Проверяем, что урок был успешно удален
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


class PaymentListApiViewTest(APITestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.course = None

    def setUp(self):
        """
        Устанавливаем начальные данные для тестов класса PaymentListApiViewTest.
        """
        self.user = User(email='user@mail.com', first_name='Пользователь')
        self.user.set_password('testpassword')
        self.user.save()

        # Создаем и сохраняем токен авторизации
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Создаем тестовый курс и урок для использования в тестах
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание тестового курса',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            description='Описание тестового урока',
            course=self.course,
            owner=self.user
        )

        # Создаем несколько платежей для тестирования
        self.payment1 = Payment.objects.create(
            user=self.user,
            payment_date='2023-08-15',
            course_or_lesson=self.course,
            amount=50.00,
            payment_method='cash'
        )
        self.payment2 = Payment.objects.create(
            user=self.user,
            payment_date='2023-08-16',
            course_or_lesson=self.course,
            amount=30.00,
            payment_method='transfer'
        )

    # Тест на просмотр списка платежей
    def test_payment_list_view(self):
        url = reverse('lessons:payment-list')  # Замените на имя URL, если оно отличается
        response = self.client.get(url)

        # Подготавливаем ожидаемые данные для сравнения
        expected_data = [
            {
                'id': self.payment1.id,
                'user': self.user.id,
                'payment_date': '2023-08-15',
                'course_or_lesson': self.course.id,
                'amount': '50.00',
                'payment_method': 'cash',
                'lessons': []

            },
            {
                'id': self.payment2.id,
                'user': self.user.id,
                'payment_date': '2023-08-16',
                'course_or_lesson': self.course.id,
                'amount': '30.00',
                'payment_method': 'transfer',
                'lessons': []

            }
        ]

        # Сравниваем ожидаемые данные с ответом сервера
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)


class CourseSubscriptionTestCase(APITestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.course1 = None
        self.course2 = None

    def setUp(self):
        """
        Устанавливаем начальные данные для тестов класса CourseSubscriptionTestCase.
        """
        self.user = User(email='user@mail.com', first_name='Пользователь')
        self.user.set_password('testpassword')
        self.user.save()

        # Создаем пользователя-модератора для тестирования прав доступа
        self.moderator = User(email='moderator@mail.com', first_name='Модератор')
        self.moderator.set_password('testpassword')
        self.moderator.save()
        self.moderator.groups.create(name='Модераторы')

        # Создаем несколько тестовых курсов для использования в тестах
        self.course1 = Course.objects.create(
            title='Курс 1',
            description='Описание курса 1',
            owner=self.user
        )
        self.course2 = Course.objects.create(
            title='Курс 2',
            description='Описание курса 2',
            owner=self.user
        )

        # Создаем подписки на курсы для тестирования
        self.course_subscription_1 = CourseSubscription.objects.create(
            owner=self.user,
            course=self.course1,
            is_subscribed=True
        )
        self.course_subscription_2 = CourseSubscription.objects.create(
            owner=self.user,
            course=self.course2,
            is_subscribed=False
        )

        # Создаем и сохраняем токен авторизации
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Создаем тестовый курс для использования в тестах
        self.course = Course.objects.create(title='Тестовый курс', description='Описание тестового курса',
                                            owner=self.user)

    # Тест на просмотр подписок пользователя
    def test_list_subscriptions_as_user(self):
        url = reverse('lessons:show_all_subscriptions')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)  # Предполагается две подписки, созданные в setUp

    # Тест на просмотр подписок модератором
    def test_list_subscriptions_as_moderator(self):
        self.client.credentials()  # Очищаем учетные данные пользователя
        refresh = RefreshToken.for_user(self.moderator)
        token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        url = reverse('lessons:show_all_subscriptions')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)  # Предполагается две подписки, созданные в setUp

    # Тест на просмотр подписок без аутентификации
    def test_list_subscriptions_unauthenticated(self):
        self.client.credentials()  # Очищаем учетные данные пользователя

        url = reverse('lessons:show_all_subscriptions')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Тест на создание подписки
    def test_create_subscription(self):
        url = reverse('lessons:subscription_create')
        data = {'course': self.course.id, 'owner': self.user.id, 'is_subscribed': True}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['course'], self.course.id)
        self.assertEqual(response.json()['owner'], self.user.id)
        self.assertEqual(response.json()['is_subscribed'], True)

    # Тест на обновление подписки
    def test_update_subscription(self):
        subscription = CourseSubscription.objects.create(course=self.course, owner=self.user, is_subscribed=False)
        url = reverse('lessons:subscription_update', args=[subscription.id])
        updated_data = {"is_subscribed": True,
                        "owner": self.user.id,
                        "course": self.course.id}

        response = self.client.put(url, data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['is_subscribed'], True)

    # Тест на удаление подписки
    def test_delete_subscription(self):
        subscription = CourseSubscription.objects.create(course=self.course, owner=self.user, is_subscribed=True)
        url = reverse('lessons:subscription_delete', args=[subscription.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CourseSubscription.objects.filter(id=subscription.id).exists())