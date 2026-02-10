import sys
import io
import os
from memvid_sdk import use

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "knowledge.mv2"
    if not os.path.exists(filename):
        print(f"Index file '{filename}' not found.")
        print("Run /memvid-rag:create to initialize the knowledge base.")
        sys.exit(1)
    with use("basic", filename, mode="open", read_only=True) as mv:
        stats = mv.stats()
        for k, v in stats.items():
            print(f"{k} : {v}")
