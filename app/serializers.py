from rest_framework import serializers
from rest_framework_mongoengine import serializers as mongo_serializers
from .validators import ValidateBookOwnership
from .models import Content, Book
from creators.serializers import ShallowCreatorSerializer
from rest_framework.validators import UniqueValidator
from django.http import Http404


class BookSerializer(mongo_serializers.DocumentSerializer):
    id = serializers.CharField(read_only=True, required=False)
    publisher = ShallowCreatorSerializer()

    class Meta:
        model = Book
        fields = ['id', 'covers','title', 'isbns', 'authors', 'active', 'publisher']
        read_only_fields = ['publisher', 'active']
        depth=2

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


class ContentSerializer(mongo_serializers.DocumentSerializer):
    id = serializers.CharField(read_only=True, 
        required=False, 
        validators=[
            UniqueValidator(queryset=Book.objects.all())
        ]
    )

    creator = ShallowCreatorSerializer()
    book = BookSerializer()
    class Meta:
        model =  Content
        fields = '__all__'
        read_only_fields = ['creator', 'active']
        validators= [ValidateBookOwnership()]
        depth=2

    def get_book_or_404(id):
        try:
            book = Book.objects.get(id=book_id)
            return book
        except Book.DoesNotExist:
            raise Http404

    def update(self,instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.images = validated_data.get('images', instance.images)
        instance.file = validated_data.get('file', instance.file)

        if 'book' in validated_data.keys():
            book_id = validated_data.get('book')
            instance.book = get_book_or_404(book_id)
        instance.save()
        return instance
        
    def create(self, validated_data):
        title = validated_data['title']
        description = validated_data['description']
        images = validated_data['images']
        creator = validated_data['creator']
        file = validated_data['file']
        book = get_book_or_404(validated_data['book']);
        instance = Content.objects.create(
            title=title,
            description=description,
            images=images,
            book=book,
            file=file,
            creator=creator
        )
        return instance

class ContentShallowSerializer(ContentSerializer):
    class Meta:
        model =  Content
        fields = ['id', 'title', 'description', 'images', 'file', 'size']


class BookDeepSerializer(BookSerializer):
    def to_representation(self, data):
        rep = super(BookSerializer, self).to_representation(data)
        content = Content.objects(book=rep['id'],active=True)
        content_serializer = ContentShallowSerializer(content, many=True)
        content = content_serializer.data
        rep['content'] = content
        return rep

        return instance