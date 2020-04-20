from rest_framework import permissions
from .models import Book, Content

class IsOwnerOfBookOrReadOnly(permissions.BasePermission):

	def has_object_permission(self, request, view, object):
		if request.method in permissions.SAFE_METHODS:
			return True
		return object.publisher == request.user

	def has_permission(self, request, view):
		if request.method == 'POST':
			if 'id' in request.data:
				book = Book.objects.get(id=request.data['id'])
				return book.publisher == request.user
		return True

class IsOwnerOfContentOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, object):
		if request.method in permissions.SAFE_METHODS:
			return True
		return object.creator == request.user
		
	def has_permission(self, request, view):
		if request.method == 'POST':
			if 'id' in request.data:
				content = Content.objects.get(id=request.data['id'])
				return content.creator == request.user
		return True
