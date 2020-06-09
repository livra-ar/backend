from django.conf.urls import url
from django.urls import path
from . import views
# TODO (Priority: LOW) : Change Creator/Content to Publisher/Content
urlpatterns = [
    url(r'^content/by-book/(?P<pk>[\w\d]+)$',
        views.book_content,
        name='book-content'
    ),
    url(r'^content/(?P<pk>[\w\d]+)$',
        views.ContentDetail.as_view(),
        name='content-detail'
    ),
    url(r'^content/$',
    	views.ContentList.as_view(),
    	name='content-list'),
    # url(r'^api/book/by-title/$',
    #     views.books_by_title,
    #     name="books-by-title"
    # ),
    url(r'^api/book/by-title/$',
        views.books_by_title,
        name="books-by-title"
    ),
    url(r'^book/(?P<pk>[\w\d]+)$',
        views.BookDetail.as_view(),
        name='book-detail'
    ),
    url(r'^book/$',
        views.BookList.as_view(),
        name='book-list'
    ),
    url(r'^publisher/books/$',
        views.PublisherBooks.as_view(),
        name='publisher-books'
    ),
    url(r'^creator/content/$',
        views.creator_content,
        name='publisher-content'
    ),


]