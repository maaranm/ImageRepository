from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

#these urls are accesible at localhost:8000/pictures/
urlpatterns = [
    path('viewall', views.view_all, name='view_all'),
    path('', views.image_upload_view, name='test'),
    path('search_object', views.object_input, name='object_input')
]