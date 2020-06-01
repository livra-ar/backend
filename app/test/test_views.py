import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from app.serializers import ContentSerializer
from app.models import *
from django.contrib.auth.hashers import check_password, make_password
client = Client()
import mongoengine
from mongoengine import connect, disconnect

    


class GetContentTest(TestCase):
    '''Test Module for GET content API'''

    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')

    def setUp(self):
       

        creator = Creator.objects.create(
        email='user@example.com',
        name='User',
        password=make_password('password')
        )

        book = Book(
            title='Book Title #1',
            authors=['Author #1'],
            isbns=['111111111111'],
            covers=['http://www.example.com/cover.png'],
            publisher=creator,

        )
        book.save()

        self.content = Content(
            title="Content Title #1",
            description="Content Description #1",
            images=['https://www.example.com/image.png'],
            creator=creator,
            book=book,
            file='https://www.example.com/file.zip'
        )

        self.content.save()
    
    def test_get_content(self):
        response = client.get(reverse('content-detail', args=(str(self.content.id),)))
        content = Content.objects.get(id=self.content.id)
        serializer = ContentSerializer(content)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)