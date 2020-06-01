# from django.test import TestCase
# from app.models import Content, Book
# from creators.models import Creator
# from django.contrib.auth.hashers import check_password, make_password

# class ContentTest(TestCase):

#     def setUp(self):
#         creator = Creator.objects.create(
#             email='user@example.com',
#             name='User',
#             password=make_password('password')
#         )

#         book = Book.objects.create(
#             title='Book Title #1',
#             authors=['Author #1'],
#             isbns=['111111111111'],
#             covers=['http://www.example.com/cover.png'],
#             publisher=creator,

#         )

#         Content.objects.create(
#             title="Content Title #1",
#             description="Content Description #1",
#             images=['https://www.example.com/image.png'],
#             creator=creator,
#             book=book,
#             file='https://www.example.com/file.zip'
#         )