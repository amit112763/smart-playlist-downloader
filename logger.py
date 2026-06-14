from datetime import datetime
import os

os.makedirs("logs", exist_ok=True)

def log_download(title):

    with open(
        "logs/download_history.log",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"{datetime.now()} | {title}\n"
        )