import os
import requests
from index import search

MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"

SYSTEM_PROMPT = """You are a music assistant. The user asks questions about current world music charts.
Based on the tracks provided, give a helpful and conversational answer.
Always mention the artist and title of the songs you recommend.
If the context doesn't contain relevant tracks, say so honestly."""

history = []

def call_mistral(messages: list[dict]) -> str:
    response = requests.post(
        MISTRAL_URL,
        headers={"Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}"},
        json={
            "model": "mistral-small-latest",
            "messages": messages,
        }
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def chat(question: str) -> str:
    tracks = search(question)
    context = "\n".join([
        f"- {t['title']} by {t['artist']} ({t['album']}): {t['description']}"
        for t in tracks
    ])

    system = f"{SYSTEM_PROMPT}\n\nRelevant tracks from the charts:\n{context}"

    messages = [
        {"role": "system", "content": system},
        *history,
        {"role": "user", "content": question},
    ]

    answer = call_mistral(messages)

    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": answer})

    return answer