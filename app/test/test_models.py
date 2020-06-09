from django.test import TestCase
from app.models import Content, Book, make_ngrams, ngrams_to_representation
from creators.models import Creator
import mongoengine
# from django.contrib.auth.hashers import check_password, make_password

class ModelTest(TestCase):


    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')

    def setUp(self):
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

        self.content_1 = Content.objects.create(
            title="Content Title #1",
            description="Content Description #1",
            images=['https://www.example.com/image.png'],
            creator=self.creator,
            book=self.book,
            file='https://www.example.com/file.zip'
        )

        self.content_2 = Content.objects.create(
            title="Content Title #2",
            description="Content Description #1",
            images=['https://www.example.com/image.png'],
            creator=self.creator,
            book=self.book,
            file='https://www.example.com/file.zip'
        )

    def test_ngrams_in_book_on_creation(self):
        ngrams = make_ngrams(self.book.title)
        self.assertEquals( ngrams_to_representation(self.book.title), self.book.ngrams)

    def test_ngrams_in_book_on_update(self):
        new_title = "New Book Title"
        ngrams = make_ngrams(new_title)
        book = self.book
        book.title = new_title
        book.save()
        self.assertEquals( ngrams_to_representation(new_title), self.book.ngrams)
