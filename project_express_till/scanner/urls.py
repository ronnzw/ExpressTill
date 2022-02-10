from django.urls import path
from scanner import views

app_name = "scanner"
urlpatterns = [
    path("camera", views.scanner_page,name="camera"),
    path('video_feed', views.video_feed, name='video_feed'),
]