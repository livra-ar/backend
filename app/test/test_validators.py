from django.test import TestCase
from app.validators import ValidateBookOwnership
from rest_framework import serializers
from app.models import *

class MockRequest():

    def __init__(self, user=None):
        self.user = user
class MockSerializer():

    def __init__(self, context):
        self.context = context

class ValidateBookOwnershipTest(TestCase):


    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')

    def setUp(self):

        self.creator1 = Creator(
        email='user2@example.com',
        name='User',
        password='password'
        )

        self.creator1.save()

        self.creator2 = Creator(
        email='user3@example.com',
        name='User2',
        password='password'
        )

        self.book = Book(
            title='Book Title #1',
            authors=['Author #1'],
            isbns=['111111111111'],
            covers=['http://www.example.com/cover.png'],
            publisher=self.creator1,

        )

        self.book.save()
        
        request = MockRequest()
        
        self.serializer = MockSerializer({
            'request': request
        })

        self.validator  = ValidateBookOwnership()
        

    def test_invalid_request(self):
        self.serializer.context['request'].user = self.creator2
        dic = {
            'book': self.book.id
        }
        self.assertRaises(serializers.ValidationError,self.validator ,dic, self.serializer)
    def test_valid_request(self):
        self.serializer.context['request'].user = self.creator1
        dic = {
            'book': self.book.id
        }
        self.validator(dic, self.serializer)