from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.hashers import check_password, make_password
from creators.models import * 

import mongoengine

client = APIClient()
class CreatorAuthTokenAndCheckEmailTest(TestCase):
    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')
        

    def setUp(self):
        self.creator_1 = Creator.objects.create(
        email='user@example.com',
        name='User',
        password= make_password('password')
        )


    def test_login_post_success(self):
        response = client.post(reverse('api_token_auth'), {
            'email': self.creator_1.email,
            'password': 'password'
        })

        token = Token.objects.get(user=self.creator_1)

        expected = {
            'id': str(self.creator_1.id),
            'name': self.creator_1.name,
            'token': token.key
        }

        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_post_non_existing_email(self):
        response = client.post(reverse('api_token_auth'), {
            'email': 'notuser@ex.com',
            'password': 'password'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_post_wrong_pass(self):
        response = client.post(reverse('api_token_auth'), {
            'email': self.creator_1.email,
            'password': 'password123'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_mail_for_existing_email(self):
        response = client.head(reverse('check-email', args=('user@example.com',)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_mail_for_non_existing_email(self):
        response = client.head(reverse('check-email', args=('notuser@example.com',)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UserViewSetTest(TestCase):
    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')
        

    def test_login_post_success(self):
        response = client.post(reverse('user-list'), {
            'name': 'Test',
            'email': 'test@example.com',
            'password': 'password'
        })

        try:
            user = Creator.objects.get(email='test@example.com')
        except Creator.DoesNotExist:
            self.fail('Creator should exist')
        
        self.assertTrue(check_password('password', user.password))
        self.assertEqual(user.name, 'Test')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

