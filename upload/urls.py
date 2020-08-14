from django.urls import path

from . import views

app_name = "upload"
urlpatterns = [
    path('index', views.index, name='index'),
    path('handleUpload', views.handleUpload, name='handleUpload'),
    path('gallery', views.gallery, name='gallery'),
    path('clearGallery', views.clearGallery, name='clearGallery'),
]