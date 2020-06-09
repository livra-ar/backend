from django.urls import reverse
from django.test import TestCase, Client
# from moderators.managers import CustomUserManager
from moderators.models import Moderator
from django.contrib.auth import get_user_model
from app.models import *
from creators.models import *
User = get_user_model()

class ContentModerationViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'mod@arplatform.com',
            'password'
        )
        self.client.login(email='mod@arplatform.com', password='password')

        self.creator = Creator.objects.create(
        email='user2@example.com',
        name='User2',
        password=('password')
        )


        self.book = Book(
            title='Book Title #1',
            authors=['Author #1'],
            isbns=['111111111111'],
            covers=['http://www.example.com/cover.png'],
            publisher=self.creator,

        )
        self.book.save()

       

        self.content_1 = Content(
            title="Content Title #1",
            description="Content Description #1",
            images=['https://www.example.com/image.png'],
            creator=self.creator,
            book=self.book,
            file='https://www.example.com/file.zip'
        )



        self.content_2 = Content(
            title="Content Title #2",
            description="Content Description #2",
            images=['https://www.example.com/image.png'],
            creator=self.creator,
            book=self.book,
            file='https://www.example.com/file.zip',
            active=False
        )

        self.content_1.save()
        self.content_2.save() 

    def tearDown(self):
        mongoengine.get_connection().drop_database('testdb')
        self.user.delete()
        
    def test_published_content_get(self):
        response = self.client.get('/admin/published-content-list/')
        self.assertEquals(response.status_code, 200)



    def test_publish_content_post(self):
        response = self.client.post('/admin/unpublished-content-list/', {
            'id': str(self.content_2.id),
            'status': 'publish'
            })
        self.assertEquals(response.status_code, 302)
        content = Content.objects.get(id=self.content_2.id)
        self.assertTrue(content.active)


    def test_unpublish_content_post(self):
        response = self.client.post('/admin/published-content-list/', {
        'id': str(self.content_1.id),
        'status': 'unpublish'
        })
        self.assertEquals(response.status_code, 302)
        content = Content.objects.get(id=self.content_1.id)
        self.assertFalse(content.active)


class BookModerationViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'mod@arplatform.com',
            'password'
        )
        self.client.login(email='mod@arplatform.com', password='password')

        self.creator = Creator.objects.create(
        email='user2@example.com',
        name='User2',
        password=('password')
        )


        self.book = Book(
            title='Book Title #1',
            authors=['Author #1'],
            isbns=['111111111111'],
            covers=['http://www.example.com/cover.png'],
            publisher=self.creator,

        )
        self.book.save()

    def tearDown(self):
        mongoengine.get_connection().drop_database('testdb')
        self.user.delete()
        
    def test_published_book_get(self):
        response = self.client.get('/admin/published-book-list/')
        self.assertEquals(response.status_code, 200)

    def test_published_book_get(self):
        response = self.client.get('/admin/unpublished-book-list/')
        self.assertEquals(response.status_code, 200)

    def test_publish_book_post(self):
        self.book.active = False
        self.book.save()

        response = self.client.post('/admin/unpublished-book-list/', {
            'id': str(self.book.id),
            'status': 'publish'
            })
        self.assertEquals(response.status_code, 302)
        book = Book.objects.get(id=self.book.id)
        self.assertTrue(book.active)


    def test_unpublish_book_post(self):
        self.book.active = True
        self.book.save()
        response = self.client.post('/admin/published-book-list/', {
            'id': str(self.book.id),
            'status': 'unpublish'
        })
        self.assertEquals(response.status_code, 302)
        book = Book.objects.get(id=self.book.id)
        self.assertFalse(book.active)

# class ModeratorLoginTests(TestCase):

#   def setUp(self):
#       self.user = User.objects.create_user(
#           'mod@arplatform.com',
#           'password'
#       )

#       self.user.save()

#   def test_login_get(self):
#       response = self.client.get(reverse('mod-login'))
#       self.assertEquals(response.status_code, 200)

#   # def test_login_post(self):
#   #   response = self.client.post(reverse('mod-login'), {
#   #       'email': 'mod@arplatform.com',
#   #       'password': 'password'  
#   #   })
#   #   self.assertEquals(response.status_code, 200)


# class ModeratorRegisterTests(TestCase):

#   def test_register_get(self):
#       response = self.client.get(reverse('mod-register'))
#       self.assertEquals(response.status_code, 200)