import tempfile

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from file_server.apps.files.models import ApiKey
from rest_framework.test import APITestCase, APIClient


class TestFileUpload(APITestCase):
    def setUp(self):
        # create and auth user
        self.password = 'admin1234'
        self.username = 'testuser'
        self.email = 'test@test.com'
        self.user = User(email=self.email, username=self.username)
        self.user.set_password('admin12345')
        self.user.save()
        self.api = ApiKey()
        self.api.owner = self.user
        self.api.save()
        self.api_key = self.api.api_key

    # django does the necessary cleanup already
    def tearDown(self):
        pass

    def test_get_files(self):
        api_client = APIClient()
        response = api_client.get(
            reverse('files', kwargs={}),
            **{
                'HTTP_AUTHORIZATION': f"ApiKey-Files {self.api_key}"
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
