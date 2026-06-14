import json
import yt_dlp

from tracker import load_progress, save_progress
from logger import log_download

def progress_hook(d):

    if d["status"] == "finished":

        title = d["info_dict"]["title"]

        index = int(
            d["info_dict"].get(
                "playlist_index",
                0
            )
        )

        save_progress(
            index,
            title,
            playlist_url
        )

        log_download(title)

        print(
            f"\nProgress Saved -> Video {index}"
        )

QUALITY_MAP = {
    360: "bestvideo[height<=360]+bestaudio/best",
    480: "bestvideo[height<=480]+bestaudio/best",
    720: "bestvideo[height<=720]+bestaudio/best",
    1080: "bestvideo[height<=1080]+bestaudio/best",
    "auto": "bestvideo+bestaudio/best"
}


def estimate_storage(resolution, videos):

    estimates = {
        360: 25,
        480: 50,
        720: 100,
        1080: 200
    }

    if resolution == "auto":
        resolution = 720

    total_mb = estimates[resolution] * videos

    return round(total_mb / 1024, 2)


def progress_hook(d):

    if d["status"] == "finished":

        title = d["info_dict"]["title"]

        index = int(
            d["info_dict"].get(
                "playlist_index",
                0
            )
        )

        save_progress(
    index,
    title,
    playlist_url
)

        log_download(title)

        print(f"\nSaved Progress -> Video {index}")


# Load Config
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

playlist_url = input(
    "\nPaste Playlist URL: "
).strip()

if not playlist_url:
    print("Playlist URL cannot be empty.")
    exit()
start_video = config["start_video"]
end_video = config["end_video"]


print("""
==================================
SMART PLAYLIST DOWNLOADER
==================================

1. New Download
2. Resume Download
3. Show Progress
4. Exit
""")

menu = input("Choice: ")

if menu == "2":

    playlist_url = input(
        "\nPaste Playlist URL: "
    ).strip()

    data = load_progress()

    start_video = (
        data["last_video"] + 1
    )

    print(
        f"\nLast Downloaded: {data['last_video']}"
    )

    print(
        f"Resume From: {start_video}"
    )

    confirm = input(
        "\nContinue? (y/n): "
    )

    if confirm.lower() != "y":
        exit()

if menu == "4":
    exit()


if menu == "3":

    data = load_progress()

    print("\n========== PROGRESS ==========")
    print("Last Video :", data["last_video"])
    print("Completed :", len(data["completed"]))
    print("==============================")

    exit()


if menu == "2":

    data = load_progress()

    start_video = data["last_video"] + 1

    print(
        f"\nResuming from video {start_video}"
    )


# Playlist Info
with yt_dlp.YoutubeDL({"extract_flat": True}) as ydl:

    info = ydl.extract_info(
        playlist_url,
        download=False
    )

playlist_name = info.get(
    "title",
    "Unknown Playlist"
)

total_videos = len(
    info.get("entries", [])
)


print("\n========== QUALITY MENU ==========")
print("1. Auto (Best Available)")
print("2. 360p")
print("3. 480p")
print("4. 720p")
print("5. 1080p")
print("==================================")


quality_choice = input(
    "Select Quality (1-5): "
)

quality_options = {
    "1": "auto",
    "2": 360,
    "3": 480,
    "4": 720,
    "5": 1080
}

resolution = quality_options.get(
    quality_choice,
    config["resolution"]
)


custom_range = input(
    "\nCustom video range? (y/n): "
)

if custom_range.lower() == "y":

    start_video = int(
        input("Start Video Number: ")
    )

    end_video = int(
        input("End Video Number: ")
    )


videos_to_download = (
    end_video - start_video + 1
)

storage = estimate_storage(
    resolution,
    videos_to_download
)


print("\n========== PLAYLIST INFO ==========")
print("Playlist :", playlist_name)
print("Total Videos :", total_videos)

if resolution == "auto":
    print("Quality : Auto")
else:
    print("Quality :", f"{resolution}p")

print("Range :", f"{start_video} -> {end_video}")
print("Videos Selected :", videos_to_download)
print("Estimated Storage :", storage, "GB")
print("===================================\n")


choice = input(
    "Start download? (y/n): "
)

if choice.lower() != "y":

    print("Download cancelled.")
    exit()


def progress_hook(d):

    if d["status"] == "finished":

        title = d["info_dict"]["title"]

        index = int(
            d["info_dict"].get(
                "playlist_index",
                0
            )
        )

        save_progress(
            index,
            title,
            playlist_url
        )

        log_download(title)

ydl_opts = {
    "format": QUALITY_MAP[resolution],
    "playliststart": start_video,
    "playlistend": end_video,
    "continuedl": True,
    "ignoreerrors": True,
    "retries": 20,
    "fragment_retries": 20,
    "progress_hooks": [
        progress_hook
    ],
    "outtmpl":
    "Downloads/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s",
}


with yt_dlp.YoutubeDL(
    ydl_opts
) as ydl:

    ydl.download(
        [playlist_url]
    )


print("\nDownload Completed.")