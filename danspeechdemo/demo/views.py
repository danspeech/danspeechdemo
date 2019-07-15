from django.http import HttpResponse, JsonResponse
from django.template import loader
import subprocess
import settings
import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .models_mapping import get_danspeech_model, get_danspeech_lm

from danspeech import Recognizer
from danspeech.audio.resources import SpeechFile

# global recognizer always running in backend
with_gpu = os.environ["DANSPEECH_GPU"] == "1"
recognizer = Recognizer(with_gpu=with_gpu)


def index(request):
    template = loader.get_template('index.html')

    # Default update model
    from danspeech.pretrained_models import Units400
    model = Units400()
    recognizer.update_model(model)

    return HttpResponse(template.render({}, request))


def preprocess_webm(request):
    old_file = os.path.join(settings.MEDIA_ROOT, "tmp.webm")
    if os.path.isfile(old_file):
        os.remove(old_file)

    audio_file = request.FILES.get('recorded_audio')
    path = default_storage.save('tmp.webm', ContentFile(audio_file.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    dest = os.path.join(settings.MEDIA_ROOT, "tmp.wav")
    command = "ffmpeg -y -i {0} -acodec pcm_s16le -ac 1 -ar 16000 -f wav {1}".format(tmp_file, dest)
    subprocess.call(command, shell=True)

    return JsonResponse({
        'success': True,
    })


def update_config(request):
    model_identifier = request.POST["model_choice"]
    lm_identifier = request.POST["language_model"]
    alpha = float(request.POST["alpha"])
    beta = float(request.POST["beta"])
    beam_width = int(request.POST["beam"])

    # Update model
    model = get_danspeech_model(model_identifier)
    recognizer.update_model(model)

    # Update lm
    lm = get_danspeech_lm(lm_identifier)
    recognizer.update_decoder(lm, alpha=alpha, beta=beta, beam_width=beam_width)

    return HttpResponse(status=204)


def encode_audio():
    with SpeechFile(filepath=os.path.join(settings.MEDIA_ROOT, "tmp.wav")) as source:
        audio = recognizer.record(source)

    return audio


def transcribe(request):
    audio = encode_audio()
    transcription = recognizer.recognize_danspeech(audio, show_all=False)
    return JsonResponse({
        'success': True,
        'trans': transcription
    })


def transcribe_google(request):
    audio = encode_audio()
    transcription = recognizer.recognize_google(audio, show_all=False)
    return JsonResponse({
        'success': True,
        'trans': transcription
    })
