from django.test import TestCase
import app.fields as CustomFields
from unittest.mock import MagicMock
from rest_framework.serializers import ValidationError
import random
from creators.models import Creator
from app.models import Book
import mongoengine

ISBNField = CustomFields.ISBNField
CreatorShallowField = CustomFields.CreatorShallowField
BookField = CustomFields.BookField


class ISBNFieldTests(TestCase):

    def setUp(self):
        self.isbn_field = ISBNField()

    def test_isbn_field_to_representation_is_string(self):
        rep_1 = self.isbn_field.to_representation('9780747532743')
        rep_2 = self.isbn_field.to_representation(9780747532743)

        assert isinstance(rep_1, str)
        assert isinstance(rep_1, str)
        self.assertEqual(rep_1, rep_2)

    def test_to_internal_value_removes_dashes(self):
        rep = self.isbn_field.to_internal_value('978-0747-532743')
        self.assertEqual(rep.count('-'), 0)

    def test_to_internal_value_with_integer(self):
        with self.assertRaises(ValidationError):
            self.isbn_field.to_internal_value(9780747532743)
            
    def test_to_internal_value_accept_valid_isbns(self):
        try:
            rep_1 = self.isbn_field.to_internal_value('978-0747-532743')
            rep_2 = self.isbn_field.to_internal_value('0747532699')
        except Exception:
            self.fail('Should not throw an error')
        
        self.assertEqual(rep_1, '9780747532743')
        self.assertEqual(rep_2, '0747532699')

    def test_to_internal_value_reject_invalid_isbns(self):
        with self.assertRaises(ValidationError):
            self.isbn_field.to_internal_value('86648636')
    
class CreatorShallowFieldTests(TestCase):

    def setUp(self):
        self.creator_field = CreatorShallowField()
        self.creator = Creator.objects.create(
            email='user@example.com',
            name='User',
            password='password'
        )

    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')

    def test_to_representation(self):
        expected = {
            'id': str(self.creator.id),
            'name': self.creator.name
        }

        self.assertEqual(self.creator_field.to_representation(self.creator), expected)


    def test_to_internal_representation_for_existing_id(self):
        _id = str(self.creator.id)
        creator = self.creator_field.to_internal_value(_id);
        self.assertEqual(self.creator.id, creator.id)


    def test_to_internal_representation_for_non_existing_id(self):
        tmp = list(str(self.creator.id))
        
        while ''.join(tmp) == str(self.creator.id):
             random.shuffle(tmp)

        _id = ''.join(tmp)
        with self.assertRaises(ValidationError):
            creator = self.creator_field.to_internal_value(_id);


class BookFieldTests(TestCase):

    def setUp(self):
        self.book_field = BookField()
        self.creator = Creator.objects.create(
            email='user@example.com',
            name='User',
            password='password'
        )

        self.book = Book.objects.create(
            title='Book Title #1',
            authors=['Author #1'],
            isbns=['111111111111'],
            covers=['http://www.example.com/cover.png'],
            publisher=self.creator,

        )

    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')

    def test_to_representation(self):
        expected = {
            'id': str(self.book.id),
            'title': self.book.title,
            'isbns': self.book.isbns,
            'authors': self.book.authors,
            'active': self.book.active,
            'covers': self.book.covers
        }

        self.assertEqual(self.book_field.to_representation(self.book), expected)


    def test_to_internal_representation_for_existing_id(self):
        _id = str(self.book.id)
        book = self.book_field.to_internal_value(_id);
        self.assertEqual(self.book.id, book.id)


    def test_to_internal_representation_for_non_existing_id(self):
        tmp = list(str(self.book.id))
        
        while ''.join(tmp) == str(self.book.id):
            random.shuffle(tmp)

        _id = ''.join(tmp)
        with self.assertRaises(ValidationError):
            creator = self.book_field.to_internal_value(_id);
