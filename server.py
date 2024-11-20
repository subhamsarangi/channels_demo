import subprocess
import datetime


def run():
    today = datetime.datetime.now().strftime("%Y%m%d")

    # Define the command to run Daphne and log output
    command = [
        "daphne",
        "backend.asgi:application",
        "--bind",
        "0.0.0.0",
        "--port",
        "8001",
        "|",  # Pipe the output to the tee command
        "tee",
        f"logs/access_{today}.log",  # Standard output log file
        "|",  # Pipe stderr
        "tee",
        f"logs/log_{today}.log",  # Standard error log file
        "2>&1",  # Redirect stderr to stdout so that tee can handle both
    ]

    # Run the command in the shell and ensure both logs are shown in terminal and saved
    subprocess.run(" ".join(command), shell=True, check=True)
