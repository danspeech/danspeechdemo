##
##  Settings that should be used when running from Docker
##

# Inherit everything from settings.py
from settings import *

ALLOWED_HOSTS = ["*"] # Give access for all domains
INSTALLED_APPS += ["sslserver"]


