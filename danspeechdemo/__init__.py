import os
import subprocess
import sys


def run_server(with_gpu=False):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    p = subprocess.Popen([str(sys.executable)] + [os.path.join(base_dir, "manage.py")] + ["runserver"])
    try:
        p.wait()
    except KeyboardInterrupt:
        p.terminate()
