# Building a dockerfile for demo purposes

In this directory  you will find a dockerfile and a build script that will
a docker container for the danspeech demo server.

It will work,  it uses a self-signed SSL certificate (necessary since otherwise
browsers will not record audio).  It is not intende for any kind of production
use and will in fact make problems even if two users use it at the same time.

That said, you can now start integrating docker components into your
danspeech-based processing pipeline.

To make this even more useful, setting up docker volumes to point to danspeech
models would be very nice, but that is not implemented in this version.  Perhaps
a later version.

