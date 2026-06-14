import json
import os

PROGRESS_FILE = "progress.json"


def load_progress():

    if not os.path.exists(PROGRESS_FILE):

        return {
            "last_video": 0,
            "completed": []
        }

    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)


def save_progress(index, title, playlist_url):

    data = load_progress()

    data["playlist_url"] = playlist_url

    data["last_video"] = index

    if title not in data["completed"]:
        data["completed"].append(title)

    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=4)