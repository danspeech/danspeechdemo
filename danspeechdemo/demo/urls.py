from . import views

from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('preprocess_audio/', views.preprocess_webm, name='preprocess_audio'),
    path('transcribe/', views.transcribe, name='transcribe'),
    path('transcribe_google/', views.transcribe_google, name='transcribe_google'),
    path('update_config/', views.update_config, name='update_config'),
    path('send_audio_filepath/', views.send_audio_filepath, name='send_audio_filepath'),
]
