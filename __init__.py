import subprocess
import sys


def run_server(with_gpu=False):
    p = subprocess.Popen([str(sys.executable)] + ["manage.py runserver"])

    try:
        p.wait()
    except KeyboardInterrupt:
        p.terminate()
