import os
import yt_dlp
import mutagen.mp4
import musicbrainzngs
from datetime import datetime

musicbrainzngs.set_useragent("retro-tv", "0.1", "your@email.com")


def fetch_metadata(song_name: str) -> dict:
    try:
        artist, title = song_name.split(" - ", 1)
        results = musicbrainzngs.search_recordings(
            recording=title.strip(),
            artist=artist.strip(),
            limit=10,
        )
        recording = results["recording-list"][0]
        release_list = recording.get("release-list", [])
        album = ""
        date = ""

        if release_list:
            def release_priority(r):
                rtype = r.get("release-group", {}).get("primary-type", "").lower()
                secondary = r.get("release-group", {}).get("secondary-type-list", [])
                if "compilation" in [s.lower() for s in secondary]:
                    return 3
                if rtype == "album": return 0
                if rtype == "single": return 1
                return 2

            best_release = None
            for r in release_list:
                release_id = r["id"]
                release = musicbrainzngs.get_release_by_id(
                    release_id, includes=["release-groups"]
                )["release"]
                r["release-group"] = release.get("release-group", {})
                r["_full"] = release
                if best_release is None or release_priority(r) < release_priority(best_release):
                    best_release = r
                if release_priority(best_release) == 0:
                    break

            album = best_release["_full"].get("title", "")
            date = best_release.get("release-group", {}).get("first-release-date", "")
            if not date:
                date = best_release["_full"].get("date", "")

        return {
            "title": recording.get("title", title.strip()),
            "artist": artist.strip(),
            "album": album,
            "date": date,
        }
    except Exception as e:
        print(f"Metadata lookup failed: {e}")
        parts = song_name.split(" - ", 1)
        return {
            "title": parts[1].strip() if len(parts) > 1 else song_name,
            "artist": parts[0].strip() if len(parts) > 1 else "",
            "album": "",
            "date": "",
        }


def embed_metadata(filepath: str, metadata: dict):
    video = mutagen.mp4.MP4(filepath)
    video["\xa9nam"] = metadata.get("title", "")
    video["\xa9ART"] = metadata.get("artist", "")
    video["\xa9alb"] = metadata.get("album", "")
    video["\xa9day"] = metadata.get("date", "")
    video.save()
    print(f"Embedded metadata: {metadata}")


def log_failure(log_path: str, song_name: str, reason: str):
    with open(log_path, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {song_name} — {reason}\n")


def download_song_video(song_name: str, output_dir: str = "downloads", archive_file: str = None, log_path: str = None):
    search_query = f"ytsearch1:{song_name} official video"

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "restrictfilenames": True,
        "quiet": False,
        # "cookiesfrombrowser": ("firefox",),
        # "js_runtimes": {"node": {"path": "/usr/bin/node"}},
    }

    if archive_file:
        ydl_opts["download_archive"] = archive_file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=True)
            entries = info.get("entries", [])
            if not entries or entries[0] is None:
                print(f"Skipping (already downloaded): {song_name}")
                return
            filepath = ydl.prepare_filename(entries[0])

        metadata = fetch_metadata(song_name)
        embed_metadata(filepath, metadata)

    except yt_dlp.utils.DownloadError as e:
        reason = str(e)
        print(f"Skipping (download failed): {song_name} — {reason}")
        if log_path:
            log_failure(log_path, song_name, reason)


def download_from_txt(filename: str, output_dir: str = "downloads"):
    # Subfolder named after input file (without extension)
    input_name = os.path.splitext(os.path.basename(filename))[0]
    subfolder = os.path.join(output_dir, input_name)
    os.makedirs(subfolder, exist_ok=True)
    print(f"Input file: {input_name}")
    print(f"Downloading into: {subfolder}")

    # Archive and log files live in the subfolder
    archive_file = os.path.join(subfolder, ".archive")
    log_path = os.path.join(subfolder, "failed.log")

    with open(filename, "r") as f:
        songs = [line.strip() for line in f if line.strip()]

    for song in songs:
        print(f"\nDownloading: {song}")
        download_song_video(song, output_dir=subfolder, archive_file=archive_file, log_path=log_path)


# --- Usage ---
# download_song_video("Eminem - Without Me")
download_from_txt("/home/stijn/Downloads/De 2012 playlist (pop).txt")