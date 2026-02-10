import sys
import io
import os
from memvid_sdk import create

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "knowledge.mv2"
    if os.path.exists(filename):
        print(f"Index file '{filename}' already exists.")
        sys.exit(0)
    mv = create(filename=filename, kind="basic", enable_vec=True, enable_lex=True)
    mv.close()
    print(f"Created index file: {filename}")
