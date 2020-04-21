from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$',
        views.login_view
    ),
     url(r'^create/$',
        views.create_view
    ),
    url(r'^list/$',
    views.list_unpublished_content)

]