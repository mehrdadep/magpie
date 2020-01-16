from rest_framework.test import APITestCase
from file_server.models import User
import tempfile

class TestFileUpload(APITestCase):
    def setUp(self):
        #create and auth user
        self.password = 'admin1234'
        self.username = 'testuser'
        self.email = 'test@test.com'
        self.user = User(email=self.email, username=self.username)
        self.user.set_password('admin12345')
        self.user.save()

        self.authenticate()

    #django does the necessary cleanup already
    def tearDown(self):
        pass

    def authenticate(self):
        url = '/admin/login'
        response = self.client.post(url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 301)

    def test_file_upload(self):
        url = '/admin/file_server/file'
        file_obj = tempfile.NamedTemporaryFile()
        file_obj.write('...')

        response = self.client.post(url, {'file': file_obj, }, format='multipart')

        self.assertEqual(response.status_code, 301)
