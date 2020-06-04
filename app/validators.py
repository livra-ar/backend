from rest_framework import serializers
from .models import Book


def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')

class ValidateBookOwnership(object):
    '''
    A class to validate the whether a book is
    owned by a user
    '''
    requires_context = True
    
    def __call__(self, value, serializer):
        print(value, serializer)
        user = serializer.context['request'].user
        if 'book' in value.keys():
            id = value['book'].id
            book = Book.objects.get(id=id)
            if book.publisher != user:
                message = 'Unauthorized book id given'
                raise serializers.ValidationError(message)