import sys
import io
from memvid_sdk import use

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def index(document_title: str, document_label: str, file_path: str, **kwargs):
    """
    Index a document into the knowledge base with vector embeddings.

    Args:
        document_title: Title of the document
        document_label: Label/category for the document
        file_path: Path to the file to index
        **kwargs: Additional arguments (e.g., embedder, enable_embedding)

    Raises:
        RuntimeError: If vector embeddings are not enabled or fail to be created
    """
    # Index the document with explicit embedding enabled
    with use(
        "basic",
        "knowledge.mv2",
        mode="auto",
        read_only=False,
        enable_vec=True,
        enable_lex=True,
    ) as mv:
        # Ensure embedding is explicitly enabled
        mv.put(
            title=document_title,
            label=document_label,
            metadata={"source": file_path},
            file=file_path,
            embedding_model=kwargs.get("embedding_model", "embed-v4.0"),
            enable_embedding=True,
        )


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python scripts/index.py <document_title> <document_label> <file_path>"
        )
        sys.exit(1)

    # Parse required arguments and optional kwargs from command line arguments
    args = sys.argv[1:]
    required_args = []
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
            required_args.append(arg)

    document_title = required_args[0]
    document_label = required_args[1]
    file_path = required_args[2]

    index(document_title, document_label, file_path, **kwargs)
