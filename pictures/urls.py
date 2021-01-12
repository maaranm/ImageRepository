from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('viewall', views.view_all, name='view_all'),
    path('upload/', views.image_upload_view, name='test'),
    path('view_object', views.image_with_object_view, name='view_object'),
    path('search_object', views.object_input, name='object_input')
]