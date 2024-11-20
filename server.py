import subprocess
import datetime


def run():
    today = datetime.datetime.now().strftime("%Y%m%d")

    command = [
        "daphne",
        "backend.asgi:application",
        "--bind",
        "0.0.0.0",
        "--port",
        "8001",
        ">",
        f"logs/access_{today}.log",  # This redirects stdout
        "2>",
        f"logs/log_{today}.log",  # This redirects stderr
    ]

    subprocess.run(" ".join(command), shell=True, check=True)
