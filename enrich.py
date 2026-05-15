import os
import requests

MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"

PROMPT = """Describe the song "{title}" by {artist} from the album "{album}" in 2-3 sentences.
Include the musical genre, mood, tempo, and typical listening context (e.g. party, workout, chill, focus).
Be concise and factual."""


def call_mistral(prompt: str) -> str:
    response = requests.post(
        MISTRAL_URL,
        headers={"Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}"},
        json={
            "model": "mistral-small-latest",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def enrich_track(track: dict) -> dict:
    prompt = PROMPT.format(
        title=track["title"],
        artist=track["artist"],
        album=track["album"],
    )
    track["description"] = call_mistral(prompt)
    return track


def enrich_all(tracks: list[dict]) -> list[dict]:
    enriched = []
    for i, track in enumerate(tracks):
        print(f"Enriching {i+1}/{len(tracks)}: {track['title']} - {track['artist']}")
        enriched.append(enrich_track(track))
    return enriched