import os
from subprocess import run


def devserver():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run(["daphne", "-b", "0.0.0.0", "-p", "8001", "progress_app.asgi:application"])
