# danspeechdemo
DanSpeech demo.

This is a demo that demonstrates some of the functionality of the [danspeech](https://github.com/danspeech/danspeech) python package. 


## Installation
Note that the demo includes some functionality of Danspeech that requires [PyAudio](https://pypi.org/project/PyAudio/) and [ctcdecoce](https://github.com/parlance/ctcdecode). 

For the best possible experience, please download and install these libraries as well! 

Else, the following will enable danspeech.

```bash
$ pip install danspeech
$ pip install django
$ git clone https://github.com/danspeech/danspeechdemo.git
$ cd danspeechdemo
$ pip install .
```


## Usage
Now, execute a script or run from terminal as below:

```bash

$ python
>>> import danspeechdemo
>>> danspeechdemo.run_server()
```

The demo will then be live at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## This demo is currently under development!

Features not working correctly:

* Streaming
* Folketinget example

These features will be added as soon as possible.

## Authors and acknowledgment
Main authors: 
* Martin Nielsen  ([martin4270@hotmail.com](martin4270@hotmail.com))
* Rasmus Arpe Fogh Jensen ([rasmus.arpe@gmail.com](rasmus.arpe@gmail.com))

This project is supported by Innovation Foundation Denmark through the projects DABAI and ATEL

Other acknowledgements:

* We've trained the models based on the code from [https://github.com/SeanNaren/deepspeech.pytorch](https://github.com/SeanNaren/deepspeech.pytorch).
* The audio handling and recognizing flow is based on [https://github.com/Uberi/speech_recognition](https://github.com/Uberi/speech_recognition).
* Handling of the pretrained models is based on [keras](https://github.com/keras-team/keras).
* We've trained all models with the aid of DTU using data from Sprakbanken ([NST](https://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-19&lang=en)).
