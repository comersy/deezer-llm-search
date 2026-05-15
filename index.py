import chromadb
from chromadb.utils import embedding_functions

COLLECTION_NAME = "tracks"

client = chromadb.Client()
ef = embedding_functions.DefaultEmbeddingFunction() # all-MiniLM-L6-v2
collection = client.get_or_create_collection(COLLECTION_NAME, embedding_function=ef)


def build_index(tracks: list[dict]) -> None:
    print("Building index...")
    collection.add(
        ids=[str(t["id"]) for t in tracks],
        documents=[t["description"] for t in tracks],
        metadatas=[{"title": t["title"], "artist": t["artist"], "album": t["album"]} for t in tracks],
    )
    print(f"Index built with {len(tracks)} tracks")


def search(query: str, n_results: int = 5) -> list[dict]:
    results = collection.query(query_texts=[query], n_results=n_results)
    return [
        {**results["metadatas"][0][i], "description": results["documents"][0][i]}
        for i in range(len(results["ids"][0]))
    ]
