from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404,JsonResponse
import binascii
import os
from rest_framework import views
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
# Create your views here.
import cloudinary
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.decorators import permission_classes, authentication_classes
from creators.authentication import TokenAuthentication

@api_view(['POST'])
@parser_classes([MultiPartParser])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def zip_upload_view(request, filename, format=None):
    file_obj = request.FILES['file']
    # TODO: Use UUID
    result = cloudinary.uploader.upload(file_obj, resource_type='auto', public_id='%s.zip' % binascii.hexlify(os.urandom(20)).decode())
    # do some stuff with uploaded file
    result = {
    'url' :'https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Placeholder_book.svg/792px-Placeholder_book.svg.png'
    }
    data = {
        'url': result['url']
    }
    return Response(data, status=201)

@api_view(['POST'])
@parser_classes([MultiPartParser])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def image_upload_view(request, filename, format=None):
    file_obj = request.FILES['file']
    # TODO: Use UUID
    result = cloudinary.uploader.upload(file_obj, resource_type='auto')
    # do some stuff with uploaded file
    print(result)
    # result = {
    # 'url' :'https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Placeholder_book.svg/792px-Placeholder_book.svg.png'
    # }
    data = {
        'url': result['url']
    }
    return Response(data, status=201)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def file_delete_view(request, id, format=None):
    public_id = id
    if public_id:
        cloudinary.uploader.destroy(public_id=public_id)
        return Response(status=201)
