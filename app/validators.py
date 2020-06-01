from rest_framework import serializers
from .models import Book

class ValidateBookOwnership(object):
    '''
    A class to validate the whether a book is
    owned by a user
    '''
    requires_context = True
    
    def __call__(self, value, serializer):
        message = 'Enter a book id you own'
        raise serializers.ValidationError(message)
        user = serializer.context['request'].user
        book = Book.objects.get(id=value['book'])
        if book.publisher != user:
            message = 'Enter a book id you own'
            raise serializers.ValidationError(message)