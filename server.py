import subprocess


def run():
    command = [
        "daphne",
        "backend.asgi:application",
        "--bind",
        "0.0.0.0",
        "--port",
        "8001",
    ]

    subprocess.run(" ".join(command), shell=True, check=True)
