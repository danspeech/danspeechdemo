from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.template import loader
import subprocess
import settings
import os
import json

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from danspeech import Recognizer
from danspeech.audio.resources import load_audio_wavPCM, load_audio, Microphone
# We need a default model. Will use the TestModel as example.
from danspeech.pretrained_models import TestModel

if "DANSPEECH_GPU" in os.environ:
    with_gpu = os.environ["DANSPEECH_GPU"] == "1"
else:
    with_gpu = False

# global recognizer always running in backend
recognizer = Recognizer(with_gpu=with_gpu)
transcriptions = []
counter = 0

def index(request):
    template = loader.get_template('index.html')
    model = TestModel()
    recognizer.update_model(model)

    return HttpResponse(template.render({}, request))


def update_config(request):
    model_identifier = int(request.POST["model_choice"])
    lm_identifier = int(request.POST["language_model"])
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


def get_danspeech_model(id):
    """
    Gets a DanSpeech model based on ID from front-end.

    We need to do it this way to avoid downloading unnecessary models.
    """

    if id == 0:
        return TestModel()
    elif id == 1:
        from danspeech.pretrained_models import DanSpeechPrimary
        return DanSpeechPrimary()
    elif id == 2:
        from danspeech.pretrained_models import Baseline
        return Baseline()
    elif id == 3:
        from danspeech.pretrained_models import TransferLearned
        return TransferLearned()
    elif id == 4:
        from danspeech.pretrained_models import Folketinget
        return Folketinget()
    elif id == 5:
        from danspeech.pretrained_models import EnglishLibrispeech
        return EnglishLibrispeech()
    else:
        print("Model identifier not valid... Defaulting to TestModel.")
        # If nothing is given, just return TestModel. Something has then gone wrong.
        return TestModel()


def get_danspeech_lm(id):
    """
    Gets a DanSpeech LM based on ID from front-end.

    We need to do it this way to avoid downloading unnecessary models.
    """

    if id == 0:
        return "greedy"
    elif id == 1:
        from danspeech.language_models import DSL3gram
        return DSL3gram()
    elif id == 2:
        from danspeech.language_models import DSL5gram
        return DSL5gram()
    elif id == 3:
        from danspeech.language_models import DSLWiki3gram
        return DSLWiki3gram()
    elif id == 4:
        from danspeech.language_models import DSLWiki5gram
        return DSLWiki5gram()
    elif id == 5:
        from danspeech.language_models import DSLWikiLeipzig3gram
        return DSLWikiLeipzig3gram()
    elif id == 6:
        from danspeech.language_models import DSLWikiLeipzig5gram
        return DSLWikiLeipzig5gram()
    elif id == 7:
        from danspeech.language_models import Wiki3gram
        return Wiki3gram()
    elif id == 8:
        from danspeech.language_models import Wiki5gram
        return Wiki5gram()
    elif id == 9:
        from danspeech.language_models import Folketinget3gram
        return Folketinget3gram()
    elif id == 10:
        from danspeech.language_models import DSL3gramWithNames
        return DSL3gramWithNames()
    else:
        print("Model identifier not valid... Defaulting to TestModel.")
        # If nothing is given, just return TestModel. Something has then gone wrong.
        return TestModel()


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


def transcribe(request):
    audio = load_audio_wavPCM(path=os.path.join(settings.MEDIA_ROOT, "tmp.wav"))
    transcription = recognizer.recognize(audio, show_all=False)
    return JsonResponse({
        'success': True,
        'trans': transcription
    })


def multi(request):
    template = loader.get_template('multi.html')
    return HttpResponse(template.render({}, request))


def send_audio_filepath(request):
    path = request.POST["path"]
    save_path = request.POST["savepath"]
    files = [f for f in os.listdir(path) if f[-3:] == "wav" or f[-4:] == "flac"]
    print(files)
    transcriptions = []
    fnames = []

    if save_path:
        save_file = open(save_path, "w", encoding="utf-8")

    for i, f in enumerate(files):

        audio = load_audio(path=os.path.join(path, f))
        transcription = recognizer.recognize(audio, show_all=False)
        transcriptions.append(transcription)
        fnames.append(f)

        if save_path:
            save_file.write(f + ": " + transcription + "\n")

        print("{0}/{1} files processed".format(i + 1, len(files)))

    if save_path:
        save_file.close()

    return JsonResponse({
        'success': True,
        'transcriptions': transcriptions,
        'fnames': fnames
    })


def update_microphone(request):
    mic_id = int(request.POST["mic_id"])
    recognizer.microphone = Microphone(sampling_rate=16000, device_index=int(mic_id))
    print("Updated mic")
    return JsonResponse({
        'success': True,
    })


def stream(request):
    template = loader.get_template('stream.html')
    from danspeech.pretrained_models import TestModel
    model = TestModel()
    recognizer.update_model(model)
    microphones = [str(m) for m in Microphone.list_microphone_names()]
    mic_list_with_numbers = list(zip(range(len(microphones)), microphones))
    mic_list = json.dumps(mic_list_with_numbers)
    print(mic_list)
    return HttpResponse(template.render({"mic_list": mic_list}, request))


def start_streaming(request):
    with recognizer.microphone as source:
        print("Adjusting for background noise")
        recognizer.adjust_for_speech(source, duration=5)

    recognizer.enable_streaming()
    generator = recognizer.streaming(recognizer.microphone)
    response = StreamingHttpResponse(generator, status=200, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response


def stop_streaming(request):
    recognizer.disable_streaming()
    return JsonResponse({
        'success': True,
    })


def streaming_generator():
    generator = recognizer.streaming(recognizer.microphone)
    while True:
        try:
            trans = next(generator)
        except StopIteration:
            break

def real_time_stream(request):
    template = loader.get_template('real_time_stream.html')
    from danspeech.pretrained_models import CPUStreamingRNN
    model = CPUStreamingRNN()
    recognizer.update_model(model)
    microphones = [str(m) for m in Microphone.list_microphone_names()]
    mic_list_with_numbers = list(zip(range(len(microphones)), microphones))
    mic_list = json.dumps(mic_list_with_numbers)
    print(mic_list)
    return HttpResponse(template.render({"mic_list": mic_list}, request))


def start_real_time_streaming(request):
    with recognizer.microphone as source:
        print("Adjusting for background noise")
        recognizer.adjust_for_speech(source, duration=5)

    recognizer.enable_real_time_streaming()
    generator = recognizer.streaming(recognizer.microphone)
    response = StreamingHttpResponse(generator, status=200, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response


def stop_real_time__streaming(request):
    recognizer.disable_streaming()
    return JsonResponse({
        'success': True,
    })
