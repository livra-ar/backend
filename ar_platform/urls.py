"""ar_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
from creators.views import *
from file_manager.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from rest_framework.authtoken.views import obtain_auth_token 	
from rest_framework import routers
# from rest_framework import 
router = routers.DefaultRouter()
from django.conf.urls import include, url
router.register(r'user', UserViewSet, r'user')
# router.register(r'book', BookViewSet, r'book')
#router.register(r'content', ContentViewSet, r'content')

urlpatterns = [
    
    # path(r'api/', )),	
    # path('content/', ContentList.as_view()),
    # path('content/<slug:pk>', ContentDetail.as_view()),
    # path('book/', BookList.as_view()),
    # path('book/<slug:pk>', BookDetail.as_view()),
    url(r'^api/v1/', include('app.urls')),
    path('user/emails/<email>/', check_email),
    path('auth/',CreatorAuthToken.as_view(), name='api_token_auth'),  # <-- And here
    path('files/delete/<id>/', file_delete_view),
    path('upload/raw/<slug:filename>', zip_upload_view),
    path('upload/img/<slug:filename>', image_upload_view),
    path('book/<slug:pk>', BookDetail.as_view()),
    path('book/', BookList.as_view()),
    path('publisher/books/', PublisherBooks.as_view()),
    path('creator/content', creator_content),
    path('content/book/<slug:pk>', book_content),
    path('content/<slug:pk>', ContentDetail.as_view()),
    path('content/', ContentList.as_view()),

    
    
    

]+ router.urls
