from creators.models import Creator
from app.models import Book
import app.serializers as AppSerializers
from rest_framework import serializers
from isbnlib import notisbn, canonical

class ISBNField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        data = canonical(data)
        if not (isinstance(data, str) or isinstance(data, int)):
            msg = 'Incorrect type. Expected a string or integer, but got %s'
            raise ValidationError(msg % type(data).__name__)
        if notisbn(data):
            raise ValidationError('Invalid ISBN')
        return str(data)

class CreatorShallowField(serializers.RelatedField):
    def get_queryset():
        return Creator.objects

    def to_representation(self, value):
        return { 'id' : str(value.id), 'name': value.name}

    def to_internal_value(self, value):
        try:
            book = self.queryset.get(id=value)
            return book
        except Creator.DoesNotExist:
            raise serializers.ValidationError('Invalid publisher id')

class BookField(serializers.RelatedField):
    def get_queryset(self):
        return Book.objects

    def to_representation(self, value):
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
