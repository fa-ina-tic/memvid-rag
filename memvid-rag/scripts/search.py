import sys
import io
from memvid_sdk import use

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def search(query: str):
    with use("basic", "knowledge.mv2", mode="auto", enable_vec=True, read_only=True) as mv:
        docs = mv.find(
            query,
            mode='hybrid'
        )
        return docs


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/search.py <query>")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    results = search(query)
    print(f"Query: {results.get('query', query)}")
    print(f"Total hits: {results.get('total_hits', 0)}")
    print(f"Took: {results.get('took_ms', 0)}ms")
    print("-" * 50)
    for hit in results.get('hits', []):
        print(hit)
        print("-" * 50)
