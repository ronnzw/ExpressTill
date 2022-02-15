from django.urls import path
from scanner import views

app_name = "scanner"
urlpatterns = [
    path("cameraa", views.scanner_page,name="camera"),
    path('video_feed', views.video_feed, name='video_feed'),
    path('camera_feed', views.camera_feed, name='camera_feed'),
    path('camera', views.detect, name='detect_barcodes'),
]