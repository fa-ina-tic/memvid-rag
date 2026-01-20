import sys
import io
from memvid_sdk import use

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def index(document_title: str, document_label: str, file_path: str, **kwargs):
    with use("basic", "knowledge.mv2", mode="auto", read_only=False) as mv:
        mv.put(
            title=document_title,
            label=document_label,
            metadata={'source':file_path},
            file=file_path,
            embedding_model='embed-v4.0',
            **kwargs
        )

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python scripts/index.py <document_title> <document_label> <file_path>")
        sys.exit(1)
    
    # Parse query and kwargs from command line arguments
    args = sys.argv[1:]
    query_parts = []
    kwargs = {}

    for arg in args:
        if arg.startswith("--"):
            # Parse --key=value format
            if "=" in arg:
                key, value = arg[2:].split("=", 1)
                # Try to convert to appropriate type
                if value.lower() in ("true", "false"):
                    kwargs[key] = value.lower() == "true"
                elif value.replace(".", "", 1).replace("-", "", 1).isdigit():
                    # Try to parse as number (int or float)
                    kwargs[key] = float(value) if "." in value else int(value)
                else:
                    kwargs[key] = value
            else:
                # Parse --key format (boolean flag)
                kwargs[arg[2:]] = True
        else:
            query_parts.append(arg)

    query = " ".join(query_parts)
    results = index(query, **kwargs)
