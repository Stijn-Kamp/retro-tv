import os
import csv
import sqlite3
import requests
import yt_dlp
import mutagen.mp4
from mutagen.mp4 import MP4Cover
from datetime import datetime


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
# SQLite
# ----------------------------

def init_db(db_path: str) -> sqlite3.Connection:
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row

    con.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            video_file        TEXT,
            cover_file        TEXT,
            title             TEXT,
            artist            TEXT,
            album             TEXT,
            album_date        TEXT,
            year              TEXT,
            duration_str      TEXT,
            bpm               REAL,
            camelot           TEXT,
            energy            REAL,
            popularity        INTEGER,
            genres            TEXT,
            dance             REAL,
            acoustic          REAL,
            instrumental      REAL,
            valence           REAL,
            speech            REAL,
            live              REAL,
            loud_db           REAL,
            key               TEXT,
            time_signature    TEXT,
            spotify_track_id  TEXT UNIQUE,
            isrc              TEXT,
            yt_id             TEXT,
            yt_channel        TEXT,
            yt_upload_date    TEXT,
            yt_duration_str   TEXT,
            yt_thumbnail      TEXT,
            added_at          TEXT,
            downloaded_at     TEXT DEFAULT (datetime('now'))
        )
    """)

    # migrate existing DBs that are missing the UNIQUE constraint
    indexes = [row[0] for row in con.execute(
        "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='songs'"
    ).fetchall()]

    if 'songs_spotify_track_id_unique' not in indexes:
        print("Migrating DB: adding UNIQUE index on spotify_track_id")
        con.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS songs_spotify_track_id_unique
            ON songs (spotify_track_id)
            WHERE spotify_track_id IS NOT NULL AND spotify_track_id != ''
        """)

    con.commit()
    return con


def upsert_song(con: sqlite3.Connection, data: dict):
    cols = ", ".join(data.keys())
    placeholders = ", ".join(f":{k}" for k in data.keys())
    updates = ", ".join(
        f"{k} = excluded.{k}"
        for k in data.keys()
        if k != "spotify_track_id"
    )
    con.execute(f"""
        INSERT INTO songs ({cols})
        VALUES ({placeholders})
        ON CONFLICT(spotify_track_id) DO UPDATE SET {updates}
    """, data)
    con.commit()


# ----------------------------
# CSV parsing
# ----------------------------

def parse_csv(filepath: str) -> list[dict]:
    songs = []
    with open(filepath, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            def get(*keys):
                for k in keys:
                    v = row.get(k, "").strip()
                    if v:
                        return v
                return ""

            album_date = get("Album Date")
            year = album_date[:4] if len(album_date) >= 4 else ""

            duration_raw = get("Duration")  # may be mm:ss or seconds
            duration_str = duration_raw if ":" in duration_raw else (
                f"{int(float(duration_raw)) // 60}:{int(float(duration_raw)) % 60:02d}"
                if duration_raw else ""
            )

            songs.append({
                "title":            get("Song"),
                "artist":           get("Artist"),
                "album":            get("Album"),
                "album_date":       album_date,
                "year":             year,
                "duration_str":     duration_str,
                "bpm":              get("BPM") or None,
                "camelot":          get("Camelot"),
                "energy":           get("Energy") or None,
                "popularity":       get("Popularity") or None,
                "genres":           get("Genres"),
                "dance":            get("Dance") or None,
                "acoustic":         get("Acoustic") or None,
                "instrumental":     get("Instrumental") or None,
                "valence":          get("Valence") or None,
                "speech":           get("Speech") or None,
                "live":             get("Live") or None,
                "loud_db":          get("Loud (Db)") or None,
                "key":              get("Key"),
                "time_signature":   get("Time Signature"),
                "spotify_track_id": get("Spotify Track Id"),
                "isrc":             get("ISRC"),
                "added_at":         get("Added At"),
            })
    return songs


# ----------------------------
# yt-dlp
# ----------------------------

def extract_yt_metadata(entry: dict) -> dict:
    upload_date = entry.get("upload_date") or ""
    duration = entry.get("duration") or 0
    duration_str = f"{duration // 60}:{duration % 60:02d}" if duration else ""

    return {
        "yt_id":          entry.get("id") or "",
        "yt_channel":     entry.get("channel") or entry.get("uploader") or "",
        "yt_upload_date": upload_date,
        "yt_duration_str": duration_str,
        "yt_thumbnail":   entry.get("thumbnail") or "",
    }


def download_cover(entry: dict, song_dir: str) -> str:
    thumbnails = entry.get("thumbnails") or []
    url = entry.get("thumbnail")

    if thumbnails:
        best = max(thumbnails, key=lambda t: (t.get("width") or 0) * (t.get("height") or 0))
        url = best.get("url") or url

    if not url:
        return ""

    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            path = os.path.join(song_dir, "cover.jpg")
            with open(path, "wb") as f:
                f.write(r.content)
            return path
    except Exception as e:
        print(f"  Cover download failed: {e}")
    return ""


def embed_metadata(filepath: str, meta: dict, cover_path: str):
    video = mutagen.mp4.MP4(filepath)
    video["\xa9nam"] = meta.get("title", "")
    video["\xa9ART"] = meta.get("artist", "")
    video["\xa9alb"] = meta.get("album", "")
    video["\xa9day"] = meta.get("album_date", "")

    if cover_path and os.path.exists(cover_path):
        with open(cover_path, "rb") as f:
            video["covr"] = [MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)]

    video.save()


# ----------------------------
# downloader
# ----------------------------

def download_song(csv_meta: dict, playlist_dir: str, con: sqlite3.Connection,
                  archive_file: str = None, log_path: str = None):

    artist = csv_meta["artist"]
    title  = csv_meta["title"]
    search_query = f"ytsearch1:{artist} - {title} Official Video"
    folder_name  = sanitize_folder_name(f"{artist} - {title}")
    song_dir     = os.path.join(playlist_dir, folder_name)
    os.makedirs(song_dir, exist_ok=True)

    output_path = os.path.join(song_dir, f"{folder_name}.%(ext)s")

    if any(
        f.endswith(".mp4")
        for f in os.listdir(song_dir)
    ):
        print(f"  ↳ Skipping (already downloaded): {artist} - {title}")
        return

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
        "cookiefile": "/home/stijn/Downloads/www.youtube.com_cookies.txt",
    }

    if archive_file:
        ydl_opts["download_archive"] = archive_file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info  = ydl.extract_info(search_query, download=True)
            entry = info["entries"][0]
            filepath = os.path.join(song_dir, os.path.basename(ydl.prepare_filename(entry)))

        # fallback: find any .mp4 in folder
        if not os.path.exists(filepath):
            for f in os.listdir(song_dir):
                if f.endswith(".mp4"):
                    filepath = os.path.join(song_dir, f)
                    break

        yt_meta   = extract_yt_metadata(entry)
        cover_path = download_cover(entry, song_dir)

        embed_metadata(filepath, csv_meta, cover_path)

        # merge CSV + yt metadata for DB
        record = {
            **csv_meta,
            **yt_meta,
            "video_file": filepath,
            "cover_file": cover_path or None,
        }
        upsert_song(con, record)

        print(f"  ✓ Done: {artist} - {title}")

    except Exception as e:
        print(f"  ✗ Failed: {artist} - {title} — {e}")
        if log_path:
            log_failure(log_path, f"{artist} - {title}", str(e))


# ----------------------------
# playlist runner
# ----------------------------

def download_from_csv(csv_path: str, output_dir: str = "media/songs"):
    playlist_name = os.path.splitext(os.path.basename(csv_path))[0]
    playlist_dir  = os.path.join(output_dir, playlist_name)
    os.makedirs(playlist_dir, exist_ok=True)

    db_path      = os.path.join(playlist_dir, "playlist.db")
    archive_file = os.path.join(playlist_dir, ".archive")
    log_path     = os.path.join(playlist_dir, "failed.log")

    con   = init_db(db_path)
    songs = parse_csv(csv_path)

    print(f"Playlist : {playlist_name}")
    print(f"Output   : {playlist_dir}")
    print(f"Database : {db_path}")
    print(f"Songs    : {len(songs)}\n")

    for i, song in enumerate(songs, 1):
        print(f"[{i}/{len(songs)}] {song['artist']} - {song['title']}")
        download_song(song, playlist_dir, con,
                      archive_file=archive_file, log_path=log_path)

    con.close()


# ----------------------------
# entry
# ----------------------------

download_from_csv(
    "/home/stijn/Downloads/The Real Slim Shady.csv",
    "media/songs"
)