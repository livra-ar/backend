from rest_framework import serializers
from .validators import ValidateBookOwnership, required
from .models import Content, Book
from creators.models import Creator
from creators.serializers import ShallowCreatorSerializer, SubCreatorSerializer
from rest_framework.validators import UniqueValidator
from django.http import Http404

from .fields import *


class BookSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(required=True)
    isbns = serializers.ListField(child=ISBNField(), allow_empty=False)
    authors = serializers.ListField(child=serializers.CharField(), allow_empty=False)
    active = serializers.BooleanField(read_only=True)
    publisher = CreatorShallowField(read_only=True)
    covers = serializers.ListField(child=serializers.URLField(), allow_empty=False)
    
    def create(self, validated_data):
        title = validated_data['title']
        isbns = validated_data['isbns']
        authors = validated_data['authors']
        covers = validated_data['covers']
        publisher = validated_data['publisher']

        instance = Book.objects.create(
            title=title,
            isbns=isbns,
            authors=authors,
            covers=covers,
            publisher=publisher
        )
        return instance

    def validate_publisher(self, value):
        try:
            publisher = Creator.objects.get(id=value)
            return publisher
        except Exception:
            raise serializers.ValidationError('Invalid publisher id')

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.isbns = validated_data.get('isbns', instance.isbns)
        instance.authors = validated_data.get('authors', instance.authors)
        instance.covers = validated_data.get('covers', instance.covers)
        instance.save()
        return instance

    
class ContentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    images = serializers.ListField(child=serializers.URLField(), allow_empty=False)
    file = serializers.URLField(required=True)
    book = BookField(required=True)
    creator = CreatorShallowField(required=False)
    active = serializers.BooleanField(required=False)
    animated = serializers.BooleanField(required=True)
    size = serializers.IntegerField(required=True)

    class Meta:
        validators = [ValidateBookOwnership()]
    def create(self, validated_data):
        title = validated_data['title']
        description = validated_data['description']
        images = validated_data['images']
        creator = validated_data['creator']
        file = validated_data['file']
        book = validated_data['book']
        size = validated_data['size']
        animated = validated_data['animated']
        instance = Content.objects.create(
            title=title,
            description=description,
            images=images,
            book=book,
            file=file,
            creator=creator,
            size=size,
            animated=animated
        )
        return instance

    def update(self,instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.images = validated_data.get('images', instance.images)
        instance.file = validated_data.get('file', instance.file)
        instance.book = validated_data.get('book', instance.book)
        instance.animated = validated_data.get('animated', instance.animated)
        instance.size = validated_data.get('size', instance.size)
        instance.save()
        return instance

class ContentShallowSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    images = serializers.ListField(child=serializers.URLField())
    file = serializers.URLField()
    active = serializers.BooleanField()
    animated = serializers.BooleanField()
    size = serializers.IntegerField()
    creator = CreatorShallowField()

class BookDeepSerializer(BookSerializer):
    def to_representation(self, data):
        rep = super(BookSerializer, self).to_representation(data)
        content = Content.objects(book=rep['id'],active=True)
        content_serializer = ContentShallowSerializer(content, many=True)
        content = content_serializer.data
        rep['content'] = content
        return rep

        return instance