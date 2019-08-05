import os
import subprocess
import sys


def run_server(with_gpu=False):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Use GPU
    if with_gpu:
        os.environ["DANSPEECH_GPU"] = "1"
    else:
        os.environ["DANSPEECH_GPU"] = "0"

    p = subprocess.Popen([str(sys.executable)] + [os.path.join(base_dir, "manage.py")] + ["runserver"],
                         env=os.environ.copy())
    try:
        p.wait()
    except KeyboardInterrupt:
        p.terminate()
