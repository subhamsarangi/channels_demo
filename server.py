import os
import subprocess


def run():
    logs_directory = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_directory, exist_ok=True)

    command = [
        "daphne",
        "backend.asgi:application",
        "--bind",
        "0.0.0.0",
        "--port",
        "8001",
    ]

    subprocess.run(" ".join(command), shell=True, check=True)
