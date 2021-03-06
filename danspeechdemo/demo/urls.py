from . import views

from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('multi_files', views.multi, name='multi_files'),
    path('stream', views.stream, name='stream'),
    path('preprocess_audio/', views.preprocess_webm, name='preprocess_audio'),
    path('transcribe/', views.transcribe, name='transcribe'),
    path('update_config/', views.update_config, name='update_config'),
    path('send_audio_filepath/', views.send_audio_filepath, name='send_audio_filepath'),
    path('update_microphone/', views.update_microphone, name='update_microphone'),
    path('start_streaming/', views.start_streaming, name='start_streaming'),
    path('stop_streaming/', views.stop_streaming, name='stop_streaming'),
]
