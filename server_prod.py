import os
import subprocess
import django


def run():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.prod")
    django.setup()
    logs_directory = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_directory, exist_ok=True)

    command = [
        "daphne",
        "backend.asgi:application",
        "--bind",
        "0.0.0.0",
        "--port",
        "8000",
    ]

    subprocess.run(" ".join(command), shell=True, check=True)
