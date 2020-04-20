from rest_framework import serializers
from .models import Book

class ValidateBookOwnership(object):
    requires_context = True
    
    def __call__(self, value, serializer):
        user = serializer.context['request'].user
        book = Book.objects.get(id=value['book'])
        if book.publisher != user:
            message = 'Enter a book id you own'
            raise serializers.ValidationError(message)
