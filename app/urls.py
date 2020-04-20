from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^content/(?P<pk>[\w\d]+)$',
        views.ContentDetail.as_view(),
        name='content-detail'
    )
]