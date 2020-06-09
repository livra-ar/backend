from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.test import TestCase, Client
from file_manager.storage_service import StorageService
import tempfile
import mongoengine
from unittest.mock import MagicMock
from creators.models import Creator

class FileManagerViewTests(APITestCase):

    def tearDown(cls):
        mongoengine.get_connection().drop_database('testdb')
        
    def setUp(self):
        self.creator_1 = Creator.objects.create(
            email='user@example.com',
            name='User',
            password= 'password'
        )

        storage_service = MagicMock(
            upload = MagicMock(return_value = {
            'secure_url' :'https://example.com/file.file'
            })
        )
        StorageService.set_instance(storage_service)

        self.tmp_file = tempfile.NamedTemporaryFile(suffix='.file')
        self.tmp_file.seek(0)

        self.client.force_authenticate(user=self.creator_1)



    def test_file_upload(self):
        response = self.client.post(reverse('content-upload', args=('filename',)), {'file': self.tmp_file}, format='multipart')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data, {
            'url': 'https://example.com/file.file'
        })

        StorageService.get_instance().upload.assert_called()

    def test_image_upload(self):
        response = self.client.post(reverse('image-upload', args=('filename',)), {'file': self.tmp_file}, format='multipart')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data, {
            'url': 'https://example.com/file.file'
        })
        StorageService.get_instance().upload.assert_called()


    def test_file_delete(self):
        response = self.client.delete(reverse('file-delete', args=('123456',)))
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        
        StorageService.get_instance().destroy.assert_called()