import os
import json
import requests
import yt_dlp
import mutagen.mp4
from mutagen.mp4 import MP4Cover
import musicbrainzngs
from datetime import datetime

musicbrainzngs.set_useragent("retro-tv", "0.1", "your@email.com")


# ----------------------------
# utils
# ----------------------------

def sanitize_folder_name(name: str) -> str:
    keep = (" ", "-", "_", ".")
    return "".join(c for c in name if c.isalnum() or c in keep).strip()


def log_failure(log_path: str, song_name: str, reason: str):
    with open(log_path, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {song_name} — {reason}\n")


# ----------------------------
# yt metadata (PRIMARY SOURCE)
# ----------------------------

def extract_entry_metadata(entry: dict) -> dict:
    upload_date = entry.get("upload_date") or ""

    year = upload_date[:4] if len(upload_date) >= 4 else ""
    date = (
        f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
        if len(upload_date) == 8
        else ""
    )

    duration = entry.get("duration") or 0
    duration_str = (
        f"{duration // 60}:{str(duration % 60).zfill(2)}"
        if duration else ""
    )

    return {
        "title": entry.get("title", "") or "",
        "artist": entry.get("channel") or entry.get("uploader") or "",
        "date": date,
        "year": year,
        "duration": duration_str,
        "release_id": entry.get("id") or "",
        "thumbnail": entry.get("thumbnail") or "",
    }


# ----------------------------
# optional enrichment (album only)
# ----------------------------

def enrich_album(song_name: str, fallback: dict) -> str:
    try:
        artist, title = song_name.split(" - ", 1)

        results = musicbrainzngs.search_recordings(
            recording=title.strip(),
            artist=artist.strip(),
            limit=5,
        )

        recs = results.get("recording-list", [])
        if not recs:
            return ""

        release_list = recs[0].get("release-list", [])
        if not release_list:
            return ""

        return release_list[0].get("title", "") or ""

    except Exception:
        return ""


# ----------------------------
# COVER DOWNLOAD (NEW)
# ----------------------------

def download_cover(entry: dict, output_dir: str) -> str:
    """
    Downloads best available thumbnail from yt_dlp entry into:
    song_dir/cover.jpg
    """

    thumbnails = entry.get("thumbnails") or []
    url = entry.get("thumbnail")

    # fallback hierarchy
    if thumbnails:
        best = max(
            thumbnails,
            key=lambda t: (t.get("width") or 0) * (t.get("height") or 0)
        )
        url = best.get("url") or url

    if not url:
        return ""

    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            path = os.path.join(output_dir, "cover.jpg")
            with open(path, "wb") as f:
                f.write(r.content)
            return path
    except Exception as e:
        print(f"Cover download failed: {e}")

    return ""


# ----------------------------
# embedding
# ----------------------------

def embed_metadata(filepath: str, meta: dict):
    video = mutagen.mp4.MP4(filepath)

    video["\xa9nam"] = meta["title"]
    video["\xa9ART"] = meta["artist"]
    video["\xa9alb"] = meta.get("album", "")
    video["\xa9day"] = meta["date"]

    # embed cover into mp4 too
    cover_path = meta.get("cover_path")
    if cover_path and os.path.exists(cover_path):
        with open(cover_path, "rb") as f:
            video["covr"] = [
                MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
            ]

    video.save()


# ----------------------------
# JSON output
# ----------------------------

def update_songs_json(output_dir: str, filename: str, meta: dict):
    json_path = os.path.join(output_dir, "metadata.json")

    songs = {}
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            songs = json.load(f)

    song_folder = os.path.dirname(os.path.join(output_dir, filename))

    src = os.path.join(song_folder, filename)
    cover = os.path.join(song_folder, "cover.jpg")

    tags = meta.get("tags") or []

    songs[filename] = {
        "src": src,
        "cover": cover,
        "title": (tags[0] if len(tags) > 0 and tags[0] else meta.get("title", "")),
        "artist": (tags[1] if len(tags) > 1 and tags[1] else meta.get("artist", "")),
        "album": (tags[2] if len(tags) > 2 and tags[2] else meta.get("album", "")),
        "date": meta.get("date", ""),
        "year": meta.get("year", ""),
        "duration": meta.get("duration", ""),
        "release_id": meta.get("release_id", ""),
    }

    with open(json_path, "w") as f:
        json.dump(songs, f, indent=2)


# ----------------------------
# downloader
# ----------------------------

def download_song_video(song_name, playlist_dir, archive_file=None, log_path=None):
    search_query = f"ytsearch1:{song_name} Official Video"

    artist, title = (song_name.split(" - ", 1) + ["Unknown"])[:2]

    safe_song_name = sanitize_folder_name(f"{artist} - {title}")

    song_dir = os.path.join(
        playlist_dir,
        safe_song_name
    )
    os.makedirs(song_dir, exist_ok=True)

    output_path = os.path.join(song_dir, f"{safe_song_name}.%(ext)s")

    ydl_opts = {
        "format": "bv*+ba/best",
        "merge_output_format": "mp4",
        "outtmpl": output_path,
        "restrictfilenames": False,
        "noplaylist": True,
        "retries": 10,
        "fragment_retries": 10,
        "socket_timeout": 30,
        "quiet": False,
        "cookiefile": "/home/stijn/Downloads/cookies.txt",    
    }

    if archive_file:
        ydl_opts["download_archive"] = archive_file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=True)

            entry = info["entries"][0]

            filepath = os.path.join(
                song_dir,
                os.path.basename(ydl.prepare_filename(entry))
            )

        if not os.path.exists(filepath):
            for f in os.listdir(song_dir):
                if f.endswith(".mp4"):
                    filepath = os.path.join(song_dir, f)
                    break

        # metadata from yt
        entry_meta = extract_entry_metadata(entry)

        # album enrichment (optional)
        entry_meta["album"] = enrich_album(song_name, entry_meta)

        # cover download (NEW)
        cover_path = download_cover(entry, song_dir)
        entry_meta["cover_path"] = cover_path

        # embed into mp4
        embed_metadata(filepath, entry_meta)

        # write JSON
        update_songs_json(song_dir, os.path.basename(filepath), entry_meta)

    except Exception as e:
        print(f"Download failed: {song_name} — {e}")

        if log_path:
            log_failure(log_path, song_name, str(e))


# ----------------------------
# playlist runner
# ----------------------------

def download_from_txt(filename: str, output_dir: str = "downloads"):
    input_name = os.path.splitext(os.path.basename(filename))[0]
    subfolder = os.path.join(output_dir, input_name)

    os.makedirs(subfolder, exist_ok=True)

    archive_file = os.path.join(subfolder, ".archive")
    log_path = os.path.join(subfolder, "failed.log")

    with open(filename, "r") as f:
        songs = [line.strip() for line in f if line.strip()]

    for song in songs:
        print(f"\nDownloading: {song}")
        download_song_video(
            song,
            playlist_dir=subfolder,
            archive_file=archive_file,
            log_path=log_path
        )


# ----------------------------
# entry
# ----------------------------

download_from_txt(
    "/home/stijn/Downloads/enimem playlist.txt",
    "media/songs"
)