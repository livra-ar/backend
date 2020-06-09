from rest_framework import status
from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.urls import reverse
from app.serializers import ContentSerializer, BookSerializer, ContentShallowSerializer, BookDeepSerializer
from app.models import *
from creators.models import *
client = APIClient()
import random
import mongoengine
from unittest.mock import MagicMock
from mongoengine import connect, disconnect
from file_manager.storage_service import StorageService


def create_user(self):
    self.creator_1 = Creator.objects.create(
    email='user@example.com',
    name='User',
    password= 'password'
    )
def create_and_store_user_and_token(self):
    create_user(self)
    self.token = Token(user=self.creator_1)
    self.token.save()
    client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


class ISBNTest(TestCase):
    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')
        
    def setUp(self):
        self.creator_1 = Creator.objects.create(
            email='user@example.com',
            name='User',
            password= 'password'
        )

        self.book_1 = Book(
            title='Book Title #1',
            authors=['Author #1'],
            isbns=['9780747532743'],
            covers=['http://www.example.com/cover.png'],
            publisher=self.creator_1,
        )
        self.book_1.save()

    def test_existing_isbn_get(self):
        isbn = '9780747532743'

        response = self.client.get(reverse('book-by-isbn', args=(isbn,)))
        book = Book.objects.get(isbns=isbn)
        serializer = BookDeepSerializer(book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_non_existing_isbn_get(self):
        isbn = '111111111112'
        response = self.client.get(reverse('book-by-isbn', args=(isbn,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {
             'error': 'Not Found'
        })


class ContentDetailTest(TestCase):
    '''Test Module for Content Detail APIView'''

    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')
        

    def setUp(self):
        StorageService.set_instance(MagicMock())

        create_and_store_user_and_token(self)

        self.creator_2 = Creator.objects.create(
        email='user2@example.com',
        name='User2',
        password=('password')
        )


        self.book_1 = Book(
            title='Book Title #1',
            authors=['Author #1'],
            isbns=['111111111111'],
            covers=['http://www.example.com/cover.png'],
            publisher=self.creator_1,

        )
        self.book_1.save()

        self.book_2 = Book(
            title='Book Title #2',
            authors=['Author #2'],
            isbns=['9780747532743'],
            covers=['http://www.example.com/cover2.png'],
            publisher=self.creator_1,

        )
        self.book_2.save()



        self.book_3 = Book(
            title='Book Title #3',
            authors=['Author #3'],
            isbns=['9780747532745'],
            covers=['http://www.example.com/cover3.png'],
            publisher=self.creator_2,

        )

        self.book_3.save()

        self.content = Content(
            title="Content Title #1",
            description="Content Description #1",
            images=['https://www.example.com/image.png'],
            creator=self.creator_1,
            book=self.book_1,
            file='https://www.example.com/file.zip'
        )

        self.content.save()


        self.content_2 = Content(
            title="Content Title #2",
            description="Content Description #2",
            images=['https://www.example.com/image2.png'],
            creator=self.creator_2,
            book=self.book_3,
            file='https://www.example.com/file_2.zip'
        )

        self.content_2.save()
    
    def test_get_content(self):
        response = client.get(reverse('content-detail', args=(str(self.content.id),)))
        content = Content.objects.get(id=self.content.id)
        serializer = ContentSerializer(content)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_content_owned_content(self):
        new_title = 'Content Title New'
        new_description = 'Content Description New'
        new_images = ['https://www.example-new.com/image.png']
        new_book = str(self.book_2.id)
        new_file = 'https://www.example-new.com/file.sfb'
        new_size = 5000
        new_animated  = True

        response = client.put(reverse('content-detail', args=(str(self.content.id),)), 
            {
                'title': new_title,
                'description' : new_description,
                'images' : new_images,
                'book' : new_book,
                'file' : new_file,
                'size' : new_size,
                'animated': new_animated
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, {
        #         'id': str(self.content.id),
        #         'title': new_title,
        #         'description' : new_description,
        #         'images' : new_images,
        #         'book' : new_book,
        #         'file' : new_file,
        #         'animated': new_animated,
        #         'size': new_size,
        #         'creator' : {
        #             'id': str(self.creator_1.id),
        #             'name': self.creator_1.name
        #         },
        #         'book':  {
        #             'id': str(self.book_2.id), 
        #             'title': self.book_2.title,
        #             'isbns': self.book_2.isbns, 
        #             'authors': self.book_2.authors, 
        #             'active': True, 
        #             'covers': self.book_2.covers
        #         },
        #         'active': True
        #     })

    def test_delete_content(self):
      
        response = client.delete(reverse('content-detail', args=(str(self.content.id),)))
        StorageService.get_instance().destroy.assert_called()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Content.DoesNotExist):
            Content.objects.get(id=self.content.id)

    '''
        Content Authorization Related Tests
    '''    
    def test_put_content_unowned_content(self):
        new_title = 'Content Title New'
        response = client.put(reverse('content-detail', args=(str(self.content_2.id),)), 
            {
                'title': new_title,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_unowned_book_to_owned_content(self):
        new_book = str(self.book_3.id)
        response = client.put(reverse('content-detail', args=(str(self.content.id),)), 
            {
                'book': new_book,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ContentListTest(TestCase):
    '''Test Module for  ContentList API View'''

    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')
    
    def setUp(self):
        create_and_store_user_and_token(self)


        self.book_1 = Book(
            title='Book Title #1',
            authors=['Author #1'],
            isbns=['111111111111'],
            covers=['http://www.example.com/cover.png'],
            publisher=self.creator_1,

        )
        self.book_1.save()


        self.creator_2 = Creator.objects.create(
            email='user2@example.com',
            name='User2',
            password=('password')
        )



        self.book_2 = Book(
            title='Book Title #3',
            authors=['Author #3'],
            isbns=['9780747532745'],
            covers=['http://www.example.com/cover3.png'],
            publisher=self.creator_2,

        )

        self.book_2.save()

    def test_post_content(self):
        new_title = 'Content Title New'
        new_description = 'Content Description New'
        new_images = ['https://www.example-new.com/image.png']
        new_book = str(self.book_1.id)
        new_file = 'https://www.example-new.com/file.sfb'
        new_size = 5000
        new_animated  = True

        response = client.post(reverse('content-list'), 
            {
                'title': new_title,
                'description' : new_description,
                'images' : new_images,
                'book' : new_book,
                'file' : new_file,
                'size' : new_size,
                'animated': new_animated
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_content_with_unowned_book(self):
        new_title = 'Content Title New'
        new_description = 'Content Description New'
        new_images = ['https://www.example-new.com/image.png']
        new_book = str(self.book_2.id)
        new_file = 'https://www.example-new.com/file.sfb'
        new_size = 5000
        new_animated  = True

        response = client.post(reverse('content-list'), 
            {
                'title': new_title,
                'description' : new_description,
                'images' : new_images,
                'book' : new_book,
                'file' : new_file,
                'size' : new_size,
                'animated': new_animated
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class BookDetailTest(TestCase):
    '''Test Module for Book Detail APIView'''

    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')
        

    def setUp(self):
        StorageService.set_instance(MagicMock())

        create_and_store_user_and_token(self)

        self.creator_2 = Creator.objects.create(
        email='user2@example.com',
        name='User2',
        password=('password')
        )



        self.book_1 = Book(
            title='Book Title #1',
            authors=['Author #1'],
            isbns=['111111111111'],
            covers=['http://www.example.com/cover.png'],
            publisher=self.creator_1,

        )
        self.book_1.save()

        self.book_2 = Book(
            title='Book Title #2',
            authors=['Author #2'],
            isbns=['9780747532743'],
            covers=['http://www.example.com/cover2.png'],
            publisher=self.creator_2,

        )
        self.book_2.save()
    
    def test_get_book(self):
        response = client.get(reverse('book-detail', args=(str(self.book_1.id),)))
        book = Book.objects.get(id=self.book_1.id)
        serializer = BookSerializer(book)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_owned_book(self):
        new_title = 'Content Title New'
        new_covers = ['https://www.example-new.com/image.png']
        new_authors = [ 'A.B. Writer' ]
        new_isbns = ['0747532699']
    

        response = client.put(reverse('book-detail', args=(str(self.book_1.id),)), 
            {
                'title': new_title,
                'covers': new_covers,
                'authors': new_authors,
                'isbns': new_isbns,
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, {
        #             'id': str(self.book_2.id), 
        #             'title': self.book_2.title,
        #             'isbns': self.book_2.isbns, 
        #             'authors': self.book_2.authors, 
        #             'active': True,
        #             'publisher': {
        #                   'id' : str(self.creator_1.id),
        #                   'name': self.creator_1.name
        #              }
        #     })

    def test_delete_book(self):
      
        response = client.delete(reverse('book-detail', args=(str(self.book_1.id),)))
        StorageService.get_instance().destroy.assert_called()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=self.book_1.id)



    '''
        Content Authorization Related Tests
    '''    
    def test_put_unowned_book(self):
        new_title = 'Book Title New'
        response = client.put(reverse('book-detail', args=(str(self.book_2.id),)), 
            {
                'title': new_title,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class BookListTest(TestCase):
    '''Test Module for  ContentList API View'''

    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')
    
    def setUp(self):
        create_and_store_user_and_token(self)


    def test_post_book(self):
        new_title = 'Book Title New'
        new_covers = ['https://www.example-new.com/image.png']
        new_authors = [ 'A.B. Writer' ]
        new_isbns = ['0747532699']
    

        response = client.post(reverse('book-list'), 
            {
                'title': new_title,
                'covers': new_covers,
                'authors': new_authors,
                'isbns': new_isbns,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class PublisherBooksTest(TestCase):
    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')
        
    def setUp(self):
        create_and_store_user_and_token(self)
        self.book_1 = Book(
            title='Book Title #1',
            authors=['Author #1'],
            isbns=['111111111111'],
            covers=['http://www.example.com/cover.png'],
            publisher=self.creator_1,

        )
        self.book_1.save()

        self.book_2 = Book(
            title='Book Title #2',
            authors=['Author #2'],
            isbns=['9780747532743'],
            covers=['http://www.example.com/cover2.png'],
            publisher=self.creator_1,

        )
        self.book_2.save()

    def test_get_publisher_books(self):
        response = client.get(reverse('publisher-books'));
        books = Book.objects(publisher=self.creator_1)
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_publisher_books_unauthorized(self):
        client.force_authenticate(user=None)
        response = client.get(reverse('publisher-books'));
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PublisherContentsTest(TestCase):
    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')
        
    def setUp(self):
        create_and_store_user_and_token(self)
        self.book_1 = Book(
            title='Book Title #1',
            authors=['Author #1'],
            isbns=['111111111111'],
            covers=['http://www.example.com/cover.png'],
            publisher=self.creator_1,

        )
        self.book_1.save()

        self.content_1 = Content(
            title="Content Title #1",
            description="Content Description #1",
            images=['https://www.example.com/image.png'],
            creator=self.creator_1,
            book=self.book_1,
            file='https://www.example.com/file.zip'
        )

        self.content_1.save()


        self.content_2 = Content(
            title="Content Title #2",
            description="Content Description #2",
            images=['https://www.example.com/image2.png'],
            creator=self.creator_1,
            book=self.book_1,
            file='https://www.example.com/file_2.zip'
        )

        self.content_2.save()
    

    def test_get_publisher_content(self):
        response = client.get(reverse('publisher-content'));
        content = Content.objects(creator=self.creator_1)
        serializer = ContentShallowSerializer(content, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_publisher_books_unauthorized(self):
        client.force_authenticate(user=None)
        response = client.get(reverse('publisher-content'));
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class BookContentsTest(TestCase):
    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')
        
    def setUp(self):
        create_user(self)

        self.book_1 = Book(
            title='Book Title #1',
            authors=['Author #1'],
            isbns=['111111111111'],
            covers=['http://www.example.com/cover.png'],
            publisher=self.creator_1,

        )
        self.book_1.save()


        self.book_2 = Book(
            title='Book Title #1',
            authors=['Author #1'],
            isbns=['111111111111'],
            covers=['http://www.example.com/cover.png'],
            publisher=self.creator_1,

        )
        self.book_2.save()

        self.content_1 = Content(
            title="Content Title #1",
            description="Content Description #1",
            images=['https://www.example.com/image.png'],
            creator=self.creator_1,
            book=self.book_1,
            file='https://www.example.com/file.zip'
        )

        self.content_1.save()

    def test_get_book_content(self):
        response = client.get(reverse('book-content', args=(str(self.book_1.id),)))
        content = Content.objects(book=self.book_1)
        serializer = ContentShallowSerializer(content, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


    def test_get_non_existing_book_content(self):
        tmp = list(str(self.book_1.id))
        
        while ''.join(tmp) == str(self.book_1.id) or ''.join(tmp) == str(self.book_2.id):
             random.shuffle(tmp)
        _id = ''.join(tmp)
        response = client.get(reverse('book-content', args=(_id,)))
        content = Content.objects(book=self.book_1)
        serializer = ContentShallowSerializer(content, many=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_get_content_from_book_without_content(self):
        response = client.get(reverse('book-content', args=(str(self.book_2.id),)))
        content = Content.objects(book=self.book_2)
        serializer = ContentShallowSerializer(content, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



'''
    Cannot Test The BookByTitle because full-text search is not supported by MongoMock
'''

class BookByISBNTest(TestCase):
    def test_title_check(self):
        response = client.post(reverse('books-by-title'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
