import requests

DEEZER_BASE = "https://api.deezer.com"

CHARTS = {
    "top100_monde": f"{DEEZER_BASE}/chart/0/tracks?limit=100",
}


def fetch_all_charts() -> list[dict]:
    print("Loading top 100 world...")
    url = f"{DEEZER_BASE}/chart/0/tracks?limit=100"
    response = requests.get(url)
    response.raise_for_status()

    tracks = []
    for track in response.json().get("data", []):
        tracks.append({
            "id": track["id"],
            "title": track["title"],
            "artist": track["artist"]["name"],
            "album": track["album"]["title"],
            "duration": track["duration"],
        })

    print(f"{len(tracks)} tracks loaded")
    return tracks


if __name__ == "__main__":
    tracks = fetch_all_charts()
    print(tracks[0])