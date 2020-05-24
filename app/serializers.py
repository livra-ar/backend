from rest_framework import serializers
from rest_framework_mongoengine import serializers as mongo_serializers
from .validators import ValidateBookOwnership
from .models import Content, Book
from rest_framework.validators import UniqueValidator
from django.http import Http404
'''
ContentSerializer
ContentWithBookSerializer
BookWithContentSerializer
BookSerializer

'''
class ContentSerializer(mongo_serializers.DocumentSerializer):
    id = serializers.CharField(read_only=True, required=False, validators=[UniqueValidator(queryset=Book.objects.all())])

    class Meta:
        model =  Content
        fields = '__all__'
        read_only_fields = ['creator', 'active']
        validators= [ValidateBookOwnership()]
        depth=2

    def to_internal_value(self, data):
        # TODO: Check if publisher can be chaged
    
        return data
    def update(self,instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.images = validated_data.get('images', instance.images)
        instance.file = validated_data.get('file', instance.file)

        if 'book' in validated_data.keys():
            bookId = validated_data.get('book')
            try:
                book = Book.objects.get(id=bookId)
                instance.book = book
            except Book.DoesNotExist:
                raise Http404
        instance.save()
        return instance
        
    def create(self, validated_data):
        title = validated_data['title']
        description = validated_data['description']
        images = validated_data['images']
        creator = validated_data['creator']
        file = validated_data['file']
        try:
            book = Book.objects.get(id=validated_data['book'])
        except Book.DoesNotExist:
            raise Http404
        instance = Content.objects.create(
            title=title,
            description=description,
            images=images,
            book=book,
            file=file,
            creator=creator
        )
        return instance

    def to_representation(self, data):
        rep = super(ContentSerializer, self).to_representation(data)
        if 'creator' in rep.keys():
            rep['creator'].pop('password')
            rep['creator'].pop('is_confirmed')
            rep['creator'].pop('is_publisher')
            rep['creator'].pop('email')

        if 'book' in rep.keys() and 'publisher' in rep['book'].keys():
            rep['book']['publisher'].pop('password')
            rep['book']['publisher'].pop('is_confirmed')
            rep['book']['publisher'].pop('is_publisher')
            rep['book']['publisher'].pop('email')
        #re.pop('password')
        return rep

class ContentShallowSerializer(ContentSerializer):
    class Meta:
        model =  Content
        fields = ['id', 'title', 'description', 'images', 'file', 'size']
class BookSerializer(mongo_serializers.DocumentSerializer):
    id = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = Book
        fields = ['id', 'covers','title', 'isbns', 'authors', 'active', 'publisher']
        read_only_fields = ['publisher']
        depth=2

    def to_internal_value(self, data):
        # # TODO: Check if publisher can be chaged
        # if ('request' in self.context.keys()) and 'publisher' not in data:
        #     data['publisher'] = self.context['request'].user
        # return data
        return data

    def to_representation(self, data):
        rep = super(BookSerializer, self).to_representation(data)
        if 'publisher' in rep.keys():
            if rep['publisher']:
                rep['publisher'].pop('password')
                rep['publisher'].pop('is_confirmed')
                rep['publisher'].pop('is_publisher')
                rep['publisher'].pop('email')
        #re.pop('password')
        return rep

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

class BookDeepSerializer(BookSerializer):
    def to_representation(self, data):
        rep = super(BookSerializer, self).to_representation(data)
        content = Content.objects(book=rep['id'],active=True)
        content_serializer = ContentShallowSerializer(content, many=True)
        content = content_serializer.data
        rep['content'] = content
        if 'publisher' in rep.keys():
            if rep['publisher']:
                rep['publisher'].pop('password')
                rep['publisher'].pop('is_confirmed')
                rep['publisher'].pop('is_publisher')
                rep['publisher'].pop('email')
        #re.pop('password')
        return rep

        return instance