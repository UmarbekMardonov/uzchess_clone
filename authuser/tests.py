from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.models import UserSettings

User = get_user_model()


class TestUserModel(TestCase):
    def test_username_generation(self):
        user = User.objects.create(phone_number='+998991231212')
        self.assertTrue(bool(user.username))

    def test_custom_username(self):
        user = User.objects.create(phone_number='+998991231212',
                                   username='testuserusername')
        self.assertEqual(user.username, 'testuserusername')

    def test_settings_created(self):
        user = User.objects.create(phone_number='+998991231212')
        self.assertTrue(UserSettings.objects.filter(user_id=user.id).exists())


class TestJwtToken(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(phone_number='+998991235555')
        self.token_url = reverse('token_obtain_pair')
        self.token_refresh_url = reverse('token_refresh')

    def test_bad_id_token(self):
        payload = {
            'id_token': 'badidtoken',
            'phone_number': self.user.phone_number
        }
        response = self.client.post(self.token_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_refresh_token(self):
    #     payload = {
    #         'refresh': 'badrefresh'
    #     }
    #     response = self.client.post(self.token_refresh_url, payload)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    #
    #
    #     refresh = RefreshToken.for_user(self.user)
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    #     response = self.client.post(self.token_refresh_url, payload)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     payload = {
    #         'refresh': str(refresh)
    #     }
    #     response = self.client.post(self.token_refresh_url, payload)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
