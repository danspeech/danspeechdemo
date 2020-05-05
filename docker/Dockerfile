FROM ubuntu:18.04

EXPOSE 8000/tcp

RUN apt-get  clean
RUN apt-get update -y
RUN apt-get  -y install git
RUN apt-get -y install apt-utils
RUN apt  install -y python3-pip
RUN apt-get -y  install python
RUN apt-get install -y ninja-build

RUN apt-get install -y libasound-dev portaudio19-dev libportaudio2
RUN apt-get install -y libsndfile1
RUN apt-get install -y ffmpeg
RUN pip3 install PyAudio

WORKDIR /workspace
COPY requirements.txt /workspace/
RUN pip3 install -r requirements.txt

WORKDIR /workspace
RUN git clone --recursive https://github.com/parlance/ctcdecode.git
WORKDIR /workspace/ctcdecode
RUN pip3 install .

WORKDIR /workspace/danspeech/danspeechdemo
COPY tmp/ /workspace/danspeech/danspeechdemo
COPY docker_settings.py  /workspace/danspeech/danspeechdemo/danspeechdemo
RUN pip3 install .

WORKDIR /workspace/danspeech/danspeechdemo/danspeechdemo
RUN python3 manage.py migrate
CMD python3 manage.py runsslserver --settings=docker_settings  0.0.0.0:8000

