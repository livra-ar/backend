from unittest.mock import MagicMock
from app.permissions import IsOwnerOfBookOrReadOnly, IsOwnerOfContentOrReadOnly
from django.test import TestCase
from app.models import *
from rest_framework import permissions
class IsOwnerOfBookOrReadOnlyTest(TestCase):

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
        self.view = MagicMock()
        self.permission = IsOwnerOfBookOrReadOnly()

    def test_has_object_permission_success_for_safe_methods(self):
        obj = MagicMock(publisher=None)
        for method in permissions.SAFE_METHODS:
            request = MagicMock(method='GET', user=self.creator1)
            self.assertTrue(self.permission.has_object_permission(request, self.view, obj))

    def test_has_object_permission_success_for_unsafe_methods(self):
        obj = MagicMock(publisher=self.creator1)
        for method in ['POST', 'PUT', 'DELETE']:
            request = MagicMock(method='POST', user=self.creator1)
            self.assertTrue(self.permission.has_object_permission(request, self.view, obj))
    
    def test_has_object_permission_failure_for_unsafe_methods(self):
        obj = MagicMock(publisher=self.creator1)
        for method in ['POST', 'PUT', 'DELETE']:
            request = MagicMock(method='POST', user=self.creator2)
            self.assertFalse(self.permission.has_object_permission(request, self.view, obj))
    
    def test_has_permission_success_for_safe_methods(self):
        for method in permissions.SAFE_METHODS:
            request = MagicMock(method='GET', user=self.creator1)
            self.assertTrue(self.permission.has_permission(request, self.view))

    def test_has_permission_success_for_unsafe_methods(self):
        for method in ['POST', 'PUT', 'DELETE']:
            request = MagicMock(method='POST', user=self.creator1)
            self.assertTrue(self.permission.has_permission(request, self.view))
    
    def test_has_permission_failure_for_unsafe_methods(self):
        for method in ['POST', 'PUT', 'DELETE']:
            request = MagicMock(method='POST', user=self.creator2, data = {
                'id': self.book.id   
            })
            self.assertFalse(self.permission.has_permission(request, self.view))


class IsOwnerOfContentOrReadOnlyTest(TestCase):

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



        self.content = Content(
            title="Content Title #1",
            description="Content Description #1",
            images=['https://www.example.com/image.png'],
            creator=self.creator1,
            book=self.book,
            file='https://www.example.com/file.zip'
        )
        self.content.save()
        self.view = MagicMock()
        self.permission = IsOwnerOfContentOrReadOnly()

    def test_has_object_permission_success_for_safe_methods(self):
        obj = MagicMock(creator=None)
        for method in permissions.SAFE_METHODS:
            request = MagicMock(method='GET', user=self.creator1)
            self.assertTrue(self.permission.has_object_permission(request, self.view, obj))

    def test_has_object_permission_success_for_unsafe_methods(self):
        obj = MagicMock(creator=self.creator1)
        
        for method in ['POST', 'PUT', 'DELETE']:
            request = MagicMock(method='POST', user=self.creator1)
            self.assertTrue(self.permission.has_object_permission(request, self.view, obj))
    
    def test_has_object_permission_failure_for_unsafe_methods(self):
        obj = MagicMock(creator=self.creator1)
        for method in ['POST', 'PUT', 'DELETE']:
            request = MagicMock(method='POST', user=self.creator2)
            self.assertFalse(self.permission.has_object_permission(request, self.view, obj))
    
    def test_has_permission_success_for_safe_methods(self):
        for method in permissions.SAFE_METHODS:
            request = MagicMock(method='GET', user=self.creator1)
            self.assertTrue(self.permission.has_permission(request, self.view))

    def test_has_permission_success_for_unsafe_methods(self):
        for method in ['POST', 'PUT', 'DELETE']:
            request = MagicMock(method='POST', user=self.creator1)
            self.assertTrue(self.permission.has_permission(request, self.view))
    
    def test_has_permission_failure_for_unsafe_methods(self):
        for method in ['POST', 'PUT', 'DELETE']:
            request = MagicMock(method='POST', user=self.creator2, data = {
                'id': self.content.id   
            })
            self.assertFalse(self.permission.has_permission(request, self.view))