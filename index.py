from sentence_transformers import SentenceTransformer
import chromadb

COLLECTION_NAME = "tracks"

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.get_or_create_collection(COLLECTION_NAME)


def build_index(tracks: list[dict]) -> None:
    print("Building index...")

    ids = [str(track["id"]) for track in tracks]
    documents = [track["description"] for track in tracks]
    metadatas = [
        {
            "title": track["title"],
            "artist": track["artist"],
            "album": track["album"],
        }
        for track in tracks
    ]
    embeddings = model.encode(documents).tolist()

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )
    print(f"Index built with {len(tracks)} tracks")


def search(query: str, n_results: int = 5) -> list[dict]:
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    tracks = []
    for i in range(len(results["ids"][0])):
        tracks.append({
            **results["metadatas"][0][i],
            "description": results["documents"][0][i],
        })
    return tracks