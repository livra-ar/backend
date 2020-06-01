from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, permissions
from .permissions import IsOwnerOfBookOrReadOnly, IsOwnerOfContentOrReadOnly
from .serializers import ContentSerializer, BookSerializer, BookDeepSerializer
from .models import Content, Book
from creators.authentication import TokenAuthentication
from rest_framework_mongoengine import viewsets
from rest_framework.decorators import authentication_classes, permission_classes,api_view

class BookList(APIView):
    authentication_classes= [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        content = Book.objects.all()
        serializer = BookSerializer(content, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        if 'id' in request.data.keys():
            del request.data['id'] 
        
        request.data['publisher'] = request.user
        serializer = BookSerializer(data=request.data,context= {'request' : request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublisherBooks(APIView):
    authentication_classes= [TokenAuthentication]

    def get_objects(self, pk):
        try:
            return Book.objects(publisher=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        books = self.get_objects(request.user)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.AllowAny])
def book_by_isbn(request, isbn, format=None):
    isbn = isbn.replace('-', '')
    try:
        book = Book.objects.get(isbns=isbn, active=True)
        serializer = BookDeepSerializer(book)
        return Response(serializer.data)
    except Book.DoesNotExist:
         return Response({
             'error': 'Not Found'
         }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.AllowAny])
def books_by_title(request, format=None):
    if 'title' not in request.data.keys():
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    title = request.data['title']
    try:
        book = Book.objects(active=True,).search_text(title).order_by('$text_score')
        serializer = BookDeepSerializer(book, many=True)
        return Response(serializer.data, headers= {'Cache-Control': 'no-cache'})
    except Book.DoesNotExist:
         return Response({
             'error': 'Not Found'
         }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def creator_content(request, format=None):
    try:
        content = Content.objects(creator=request.user)
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)
    except Content.DoesNotExist:
        raise Http404


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def book_content(request, pk, format=None):
    try:
        book = Book.objects.get(id = pk)
        content = Content.objects(book = book, active=True)
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)
    except Content.DoesNotExist:
        raise Http404
    except Book.DoesNotExist:
        raise Http404

class BookDetail(APIView):
    authentication_classes= [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOfBookOrReadOnly]
    def get_object(self, pk):
        try:
            return Book.objects.get(id=pk)
        except Book.DoesNotExist:
            raise Http404
    
    def get_active_object(self, pk, request):
        try:
            book = Book.objects.get(id=pk)
            if book:
                if book.publisher != request.user and not book.active:
                    raise Http404
                else:
                    return book
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        try:
            book = self.get_active_object(pk, request)
        except:
            raise Http404
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        self.check_object_permissions(request, book)
        serializer = BookSerializer(book, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def patch(self, request, pk, format=None):
    #       book = self.get_object(pk)
    #       serializer = BookSerializer(book, request.data, partial=True)

    #       if serializer.is_valid():
    #           serializer.save()
    #           return Response(serializer.data)
    #       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        self.check_object_permissions(request, book)
        book.delete()
        #delete images from storage & clear index
        return Response(status=status.HTTP_204_NO_CONTENT)

class ContentList(APIView):
    authentication_classes= [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        content = Content.objects.all()
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if 'id' in request.data.keys():
            del request.data['id'] 
        request.data['creator'] = request.user
        serializer = ContentSerializer(data=request.data,context= {'request' : request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContentDetail(APIView):
    authentication_classes= [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOfContentOrReadOnly]

    def get_object(self, pk):
        try:
            return Content.objects.get(id=pk)
        except Content.DoesNotExist:
            raise Http404
    
    def get_active_object(self, pk, request):
        try:
            content = Content.objects.get(id=pk)
            if content:
                if content.creator != request.user and not content.active:
                    return Http404
                else:
                    return content      
        except Content.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        content = self.get_active_object(pk, request)
        serializer = ContentSerializer(content)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        content = self.get_object(pk)
        self.check_object_permissions(request, content)

        serializer = ContentSerializer(content, request.data, context={'request':request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def patch(self, request, pk, format=None):
    #       content = self.get_object(pk)
    #       serializer = ContentSerializer(content, request.data, partial=True)

    #       if serializer.is_valid():
    #           serializer.save()
    #           return Response(serializer.data)
    #       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        content = self.get_object(pk)
        self.check_object_permissions(request, content)
        content.delete()
        #todo delete images from storage
        return Response(status=status.HTTP_204_NO_CONTENT)
