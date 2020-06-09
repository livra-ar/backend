from creators.models import Creator
from app.models import Book

from rest_framework import serializers
from isbnlib import notisbn, canonical

class ISBNField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        if not (isinstance(data, str)):
            msg = 'Incorrect type. Expected a string, but got %s'
            raise serializers.ValidationError(msg % type(data).__name__)
        if notisbn(data):
            raise serializers.ValidationError('Invalid ISBN')
        data = canonical(data)  
        return str(data)

class CreatorShallowField(serializers.RelatedField):
    def get_queryset(self):
        return Creator.objects

    def to_representation(self, value):
        return { 'id' : str(value.id), 'name': value.name}

    def to_internal_value(self, value):
        try:
            book = self.get_queryset().get(id=value)
            return book
        except Creator.DoesNotExist:
            raise serializers.ValidationError('Invalid publisher id')

class BookField(serializers.RelatedField):
    def get_queryset(self):
        return Book.objects

    def to_representation(self, value):
        import app.serializers as AppSerializers
        serializer = AppSerializers.BookSerializer(value)
        dic = serializer.data
        del dic['publisher']
        return dic

    def to_internal_value(self, value):
        try:
            book = self.get_queryset().get(id=value)
            return book
        except Book.DoesNotExist:
            raise serializers.ValidationError('Invalid book id')
