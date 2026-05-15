from dotenv import load_dotenv
load_dotenv()

from fetch import fetch_all_charts
from enrich import enrich_all
from index import build_index
from chat import chat


def main():
    print("=== charts-chat ===\n")

    tracks = fetch_all_charts()
    tracks = enrich_all(tracks)
    build_index(tracks)

    print("\nReady! Ask me anything about the current world charts.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() == "exit":
            break
        answer = chat(question)
        print(f"\nAssistant: {answer}\n")


if __name__ == "__main__":
    main()