from django.contrib.auth.models import User
from django.test import TestCase, Client


class TestLoginView(TestCase):

    def setUp(self):
        user1 = User.objects.create_user(
            username='test1',
            email='test_email1@test1.org',
            first_name='A',
            last_name='B',
            password='password'
        )
        self.login_url = '/login/'

    def test_on_successful_login(self):
        client = Client()
        response = client.post(
            self.login_url,
            {
                'username': 'test1',
                'password': 'password'
            }
        )

        self.assertEqual(response.status_code, 302)
